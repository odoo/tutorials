from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    # =====================================
    # Field Definitions
    # =====================================
    coation_ids = fields.Many2one("coatations.claims", readonly=True)
    type_of_price = fields.Selection(
        selection=[
            ("regular", "Regular price"),
            ("coatation", "Coatation price"),
            ("last", "Last selling price"),
        ],
        default="regular",
        required=True,
        string="Type of price:",
        compute="_compute_type_of_price",
        store=True,
    )

    # =====================================
    # Computation Methods
    # =====================================
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
                    ]  # Assuming only one coatation line per product for that customer

                    # Get the min and max quantities from the coatation line
                    min_qty = coatation_line.min_qty
                    print("Min quantity is:", min_qty)
                    max_qty = coatation_line.max_qty
                    print("Max quantity is:", max_qty)

                    # Check if the quantity is within the valid range
                    if min_qty <= line.product_uom_qty <= max_qty:
                        # If quantity is within range, retain the coatation price
                        line.type_of_price = "coatation"
                        line.price_unit = coatation_line.recommended_sp
                        print("Checking if price is lower than SP:")
                        print("Recommended price is:", coatation_line.recommended_sp)
                        print("Unit price is:", line.price_unit)
                    else:
                        # If quantity is out of bounds, revert to the regular price
                        line.type_of_price = "regular"
                        line.price_unit = line.product_id.list_price
                else:
                    # If no matching coatation line is found, fallback to regular price
                    line.type_of_price = "regular"
                    line.price_unit = line.product_id.list_price
            else:
                # If no coatation_ids are set, fallback to regular price
                line.type_of_price = "regular"
                line.price_unit = line.product_id.list_price
