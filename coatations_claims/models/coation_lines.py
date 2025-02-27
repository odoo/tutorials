from odoo import api, fields, models


class CoationsClaims(models.Model):
    _name = "coatations.lines"
    _description = "List of all coations"
    product_id = fields.Many2one("product.product")
    coatation_unit_price = fields.Float()
    max_qty = fields.Integer()
    min_qty = fields.Integer()
    qty_per_order = fields.Integer()
    recommended_sp = fields.Float()
    consumed = fields.Integer()
    status = fields.Selection(
        string="state", selection=[("active", "Active"), ("expired", "Expired")]
    )
    claim = fields.Boolean()
    coation_id = fields.Many2one("coatations.claims")
    internal_reference = fields.Char(compute="_compute_internal_reference")

    _sql_constraints = [
        # Ensuring max_qty is positive
        (
            "positive_max_qty",
            "CHECK(max_qty > 0)",
            "Maximum quantity must be greater than zero!",
        ),
        # Ensuring min_qty is positive
        (
            "positive_min_qty",
            "CHECK(min_qty > 0)",
            "Minimum quantity must be greater than zero!",
        ),
        # Ensuring qty_per_order is positive
        (
            "positive_qty_per_order",
            "CHECK(qty_per_order > 0)",
            "Quantity per order must be greater than zero!",
        ),
        # Ensuring coatation_unit_price is positive
        (
            "positive_coatation_unit_price",
            "CHECK(coatation_unit_price > 0)",
            "Coatation unit price must be greater than zero!",
        ),
        # Ensuring max_qty is greater than min_qty
        (
            "max_more_than_min",
            "CHECK(max_qty > min_qty)",
            "Maximum quantity should be more than minimum quantity!",
        ),
        # Ensuring recommended_sp is positive
        (
            "positive_recommended_sp",
            "CHECK(recommended_sp > 0)",
            "Recommended selling price must be greater than zero!",
        ),
        # Ensuring max_qty is greater than or equal to consumed
        (
            "max_qty_greater_than_consumed",
            "CHECK(max_qty >= consumed)",
            "Maximum quantity must be greater than or equal to consumed quantity!",
        ),
        # Ensuring consumed quantity is greater than zero
        (
            "positive_consumed_qty",
            "CHECK(consumed > 0)",
            "Consumed quantity must be greater than zero!",
        ),
    ]

    @api.depends("coation_id")
    def _compute_internal_reference(self):
        for reference in self.coation_id:
            if reference and reference.name != "New":
                self.internal_reference = reference.name
            else:
                self.internal_reference = ""
