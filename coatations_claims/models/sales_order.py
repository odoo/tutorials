from odoo import api, fields, models
from odoo import Command


class SaleOrder(models.Model):
    _inherit = ["sale.order.line"]

    coation_ids = fields.Many2one("coatations.claims", readonly=True)
    type_of_price = fields.Selection(
        selection=[
            ("regular", "Regular price"),
            ("coatation", "Coatation price"),
            ("last", "Last selling price"),
        ],
        default="regular",
        required=True,
        readonly=True,
        string="Type of price:",
        compute="_compute_type_of_price",
        store=True,
    )
    price_approval_created = fields.Boolean(
        string="Approval Created",
        default=False,
        store=True,
        compute="_compute_approval",
    )

    def _create_price_approval_request(
        self, line, recommended_price, coatation, sale_order
    ):
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
            "product_line_ids": [Command.create({"product_id": line.product_id.id})],
        }
        self.env["approval.request"].create(approval_vals)
        print("approvals have been created!")

    @api.depends("product_uom_qty", "coation_ids")
    def _compute_type_of_price(self):
        for line in self:
            if line.coation_ids:  # Ensure that there is a related coation record
                # Fetch the corresponding coatation line based on the product
                coatation_line = line.coation_ids.coation_lines_ids.filtered(
                    lambda l: l.product_id == line.product_id
                )
                # Check if there is a matching coatation line
                if coatation_line:
                    coatation_line = coatation_line[
                        0
                    ]  # Assuming only one coatation line for the product

                    # Get the min and max quantities from the coatation line
                    min_qty = coatation_line.min_qty
                    print("min quantity is:")
                    print(min_qty)
                    max_qty = coatation_line.max_qty
                    print("max qty is")
                    print(max_qty)

                    # Check if the quantity is within the valid range
                    if min_qty <= line.product_uom_qty <= max_qty:
                        # If quantity is within range, retain the coatation price
                        line.type_of_price = "coatation"
                        line.price_unit = coatation_line.recommended_sp
                        print("checking if price is lower than sp")
                        print("recommended price is:")
                        print(coatation_line.recommended_sp)
                        print("unit price is:")
                        print(line.price_unit)
                        print(line.price_approval_created)
                        # if line.price_unit < coatation_line.recommended_sp and not line.price_approval_created:
                        #     print("creating approval!!!")
                        #     self._create_price_approval_request(line, coatation_line.recommended_sp, line.coation_ids, line.order_id)
                        #     line.price_approval_created = True # Set the flag to True after creating approval to avoid creating double approvals 1 when changed and one when saving.
                    else:
                        # If quantity is out of bounds, revert to the regular price
                        line.type_of_price = "regular"
                        # Revert the price to the regular price
                        line.price_unit = line.product_id.list_price
                        line.price_approval_created = (
                            False  # Reset approval flag if price is reset
                        )
                else:
                    # If no matching coatation line is found, fallback to regular price
                    line.type_of_price = "regular"
                    line.price_unit = line.product_id.list_price
                    line.price_approval_created = (
                        False  # Reset approval flag if price is reset
                    )
            else:
                # If no coatation_ids are set, fallback to regular price
                line.type_of_price = "regular"
                line.price_unit = line.product_id.list_price
                line.price_approval_created = (
                    False  # Reset approval flag if no coatation_ids
                )

    @api.depends("price_unit")
    def _compute_approval(self):
        for line in self:
            if line.coation_ids:
                # Find the matching coatation line for this product
                coatation_line = line.coation_ids.coation_lines_ids.filtered(
                    lambda l: l.product_id == line.product_id
                )
                if coatation_line:
                    recommended_price = coatation_line.recommended_sp

                    # Check if the price is lower than the recommended price and if approval has not been created
                    if line.price_unit < recommended_price:
                        self._create_price_approval_request(
                            line,
                            coatation_line.recommended_sp,
                            line.coation_ids,
                            line.order_id,
                        )
                        line.price_approval_created = True
                        line.order_id.isApproved = (
                            False  # for confirm button and ribbon
                        )
                    elif line.price_unit >= recommended_price:
                        # If price is above or equal to the recommended price, reset the approval flag
                        line.price_approval_created = False
                        line.order_id.isApproved = (
                            False  # for confirm button and ribbon
                        )
