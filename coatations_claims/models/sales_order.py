from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    # Fields
    approved = fields.Boolean(default=True)

    # ============================
    # Private Functions
    # ============================

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
    # Write Method to Handle Approval Requests
    # ============================

    def write(self, vals):
        """Override the write method to handle approval requests based on price changes."""
        if "partner_id" in vals:
            # Clear the coation_ids for all order lines when partner_id is changed
            for order in self:
                for line in order.order_line:
                    line.coation_ids = None  # Clear the coation_ids on the order line
                    # approved is set to false in case previous client was in approval state and now the client has been changed this will remove the to be approved ribbon in gui.
                    line.order_id.approved = False
            return super(SaleOrder, self).write(vals)

        if "order_line" in vals:
            for line in vals["order_line"]:
                # Ensure that line is a list
                if isinstance(line, list):
                    price_unit = None
                    line_id = line[
                        1
                    ]  # Index one because line ID is always on 1 index no matter the changes.

                    # Iterate over the list to find the dictionary with 'price_unit' and the line ID
                    for item in line:
                        if isinstance(item, dict):
                            if "price_unit" in item:
                                price_unit = item["price_unit"]

                    # Check if both price_unit and line_id are found
                    if price_unit is not None and line_id is not None:
                        # Get the sale order line record based on the line ID
                        line_record = self.env["sale.order.line"].browse(line_id)

                        # Check if the sale order line has coation_ids
                        if line_record.coation_ids:
                            # Find the matching coatation line for this product
                            coatation_line = (
                                line_record.coation_ids.coation_lines_ids.filtered(
                                    lambda l: l.product_id == line_record.product_id
                                )
                            )

                            if coatation_line:
                                recommended_price = coatation_line.recommended_sp

                                # Check if the price is lower than the recommended price
                                if price_unit < recommended_price:
                                    # Create approval request if needed
                                    self._create_price_approval_request(
                                        line_record,
                                        recommended_price,
                                        line_record.coation_ids,
                                        line_record.order_id,
                                    )
                                    # Set approval to False
                                    line_record.order_id.approved = False

        # Call the super method to ensure the original write behavior is preserved
        return super(SaleOrder, self).write(vals)

    # ============================
    # Constraint Function
    # ============================

    @api.constrains("state")
    def _check_quotation_expiry(self):
        """
        This method checks if any of the associated coatation lines have expired.
        If any of the quotations have expired, it raises an exception.
        """
        for order in self:
            for line in order.order_line:
                if line.coation_ids:
                    matching_coatation_lines = self.env["coatations.lines"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            ("coation_id.client_id", "=", order.partner_id.id),
                            ("status", "=", "expired"),
                            ("coation_id", "=", line.coation_ids.id),
                        ]
                    )
                    if matching_coatation_lines:
                        breakpoint()
                        if (
                            not matching_coatation_lines.max_qty
                            == matching_coatation_lines.consumed
                        ) or self.state != "sale":
                            raise ValidationError(
                                f"The quotation for product '{line.product_id.name}' has expired or you are using above max quantity. Please create or select a new quotation for this client if you want to proceed."
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
                        f"The quotation for product '{coatation_line.product_id.name}' has expired. Please create a new quotation.".format(
                            coatation_line.product_id.name
                        )
                    )
        return super(SaleOrder, self).create(vals)
