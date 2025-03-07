from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    # Fields
    approved = fields.Boolean(default=True, compute="_compute_approval", store=True)
    activity_created = fields.Boolean()
    expired = fields.Boolean()

    # ============================
    # Private Functions
    # ============================

    def _create_activity_for_expired_quotation(self, coatation_line):
        """
        Creates an activity to remind the user about the expired quotation.
        This activity will be linked to the related partner (customer) of the quotation.
        """
        print("CREATING ACTIVITY!!!!!!!!!!")
        # Create an activity (e.g., a todo task) for the expired quotation
        activity_type = self.env["mail.activity.type"].search(
            [("id", "=", "4")], limit=1
        )

        if not activity_type:
            raise ValidationError("No 'To Do' activity type found.")

        # Create the activity linked to the partner (customer)
        self.env["mail.activity"].create(
            {
                "summary": f" Finalize quotation for product '{coatation_line.product_id.name}'",
                "activity_type_id": activity_type.id,
                "res_model_id": self.env["ir.model"]._get_id("sale.order"),
                "res_id": self.id,  # Customer related to the quotation
                "date_deadline": coatation_line.coation_id.date_to,  # You can adjust this date based on your business logic
                "user_id": self.env.user.id,  # Activity assigned to the current user
                "res_name": self.name,
            }
        )
        print(
            f"Activity created for expired quotation for product '{coatation_line.product_id.name}'."
        )

    def _create_price_approval_request(
        self, line, recommended_price, coatation, sale_order
    ):
        """
        Creates an approval request when the unit price is lower than the recommended price.
        """
        print("approval function called!")
        approval_vals = {
            "name": f"Price approval for Coatation ID: {coatation.name}",
            "category_id": 3,
            "reason": f"Price {line.price_unit} is lower than recommended price {recommended_price}. "
            f"Coatation ID: {coatation.name}, Sale Order ID: {sale_order.name}",
            "partner_id": sale_order.partner_id.id,
            "reference": sale_order.name,
            "request_status": "pending",
            "product_line_ids": [Command.create({"product_id": line.product_id.id})],
        }
        self.env["approval.request"].sudo().create(approval_vals)
        print("approvals have been created!")

    # ============================
    # Compute and Onchange Functions
    # ============================

    @api.depends("order_line.price_unit")
    def _compute_approval(self):
        for line in self.order_line:
            if line.coation_ids:
                # Find the matching coatation line for this product
                coatation_line = line.coation_ids.coation_lines_ids.filtered(
                    lambda l: l.product_id == line.product_id
                )
                if coatation_line:
                    recommended_price = coatation_line.recommended_sp

                    # Check if the price is lower than the recommended price and if approval has not been created
                    if line.price_unit < recommended_price:
                        # checking if we are not working in cache memory to only call approval function when saved
                        if not isinstance(line.id, models.NewId):
                            self._create_price_approval_request(
                                line,
                                coatation_line.recommended_sp,
                                line.coation_ids,
                                line.order_id,
                            )

                        self.approved = False  # for confirm button and ribbon
                        print("printing approval boolean!")
                        print(line.order_id.approved)

                    elif line.price_unit >= recommended_price:
                        # If price is above or equal to the recommended price, reset the approval flag
                        self.approved = True  # for confirm button and ribbon
                        print("printing approval boolean")
                        print(line.order_id.approved)
                        print("activity created state is:", self.activity_created)
                        print(
                            "coation state for activity_creation is",
                            coatation_line.coation_id.state,
                        )

                    if recommended_price:
                        self._create_activity_for_expired_quotation(coatation_line)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Clears coation_id and resets prices when the customer (partner) changes."""
        for order_line in self.order_line:
            # Check if there's a quotation line linked to this order line
            if order_line.coation_ids:
                print(order_line.coation_ids)
                # Clear the coatation line (set coation_id to False)
                order_line.coation_ids = None
                order_line.type_of_price = "regular"
                # Reset the price to the product's regular price
                order_line.price_unit = order_line.product_id.list_price
                order_line.write(
                    {
                        "coation_ids": None,
                        "price_unit": order_line.product_id.list_price,
                        "type_of_price": "regular",
                    }
                )
                print(
                    f"Reverted price for product {order_line.product_id.name} to regular price."
                )

    # ============================
    # constraint function
    # ============================

    @api.constrains("state")
    def _check_quotation_expiry(self):
        """
        This method checks if any of the associated coatation lines have expired.
        If any of the quotations have expired, it raises an exception.
        """
        for order in self:
            for line in order.order_line:
                # Check if the sale order line is linked to a quotation (CoationsLines)
                if line.coation_ids:
                    # Search for the related CoationsLines for the same product and the same client
                    matching_coatation_lines = self.env["coatations.lines"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            (
                                "coation_id.client_id",
                                "=",
                                order.partner_id.id,
                            ),  # client_id is from coation_id
                            (
                                "status",
                                "=",
                                "expired",
                            ),  # Check if the status is expired
                            ("coation_id", "=", line.coation_ids.id),
                        ]
                    )
                    # If any expired quotation is found, raise validation error
                    if matching_coatation_lines:
                        self.expired = True
                        raise ValidationError(
                            "The quotation for product '{}' has expired. Please create or select a new quotation for this client.".format(
                                line.product_id.name
                            )
                        )

    # ============================
    # Action Overrides
    # ============================

    @api.model_create_multi
    def create(self, vals):
        # Ensure that expired quotations don't get linked during creation
        if "order_line" in vals:
            for order_line in vals["order_line"]:
                coatation_line = self.env["coatations.lines"].browse(
                    order_line.get("coatation_line_id")
                )
                if coatation_line and coatation_line.state == "expired":
                    raise ValidationError(
                        "The quotation for product '{}' has expired. Please create a new quotation.".format(
                            coatation_line.product_id.name
                        )
                    )
        return super(SaleOrder, self).create(vals)

    def action_confirm(self):
        """Override action_confirm to include the quotation expiry check."""
        self._check_quotation_expiry()
        return super(SaleOrder, self).action_confirm()

    def action_quotation_send(self):
        """Override to add quotation expiry check before sending."""
        self._check_quotation_expiry()
        return super(SaleOrder, self).action_quotation_send()

    def action_cancel(self):
        """Override cancel action to ensure expired quotations aren't processed."""
        self._check_quotation_expiry()
        return super(SaleOrder, self).action_cancel()
