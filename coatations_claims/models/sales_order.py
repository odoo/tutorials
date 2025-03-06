from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ["sale.order"]
    approved = fields.Boolean(default=True, compute="_compute_approval", store=True)

    def _create_price_approval_request(
        self, line, recommended_price, coatation, sale_order
    ):
        print("approval function called!")
        """
        Creates an approval request when the unit price is lower than the recommended price.
        """
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
                        raise ValidationError(
                            "The quotation for product '{}' has expired. Please create or select a new quotation for this client.".format(
                                line.product_id.name
                            )
                        )

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
                        # checking if we are not working in cache memory to only call apporval function when saved.
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
                        print("printing approval boolean")
                        self.approved = True  # for confirm button and ribbon
                        print(line.order_id.approved)
