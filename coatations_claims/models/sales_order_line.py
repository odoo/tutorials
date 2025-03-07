from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
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
                    else:
                        # If quantity is out of bounds, revert to the regular price
                        line.type_of_price = "regular"
                        # Revert the price to the regular price
                        line.price_unit = line.product_id.list_price
                else:
                    # If no matching coatation line is found, fallback to regular price
                    line.type_of_price = "regular"
                    line.price_unit = line.product_id.list_price
            else:
                # If no coatation_ids are set, fallback to regular price
                line.type_of_price = "regular"
                line.price_unit = line.product_id.list_price
