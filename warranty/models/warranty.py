from odoo import fields, models


class Warranty(models.Model):
    _name = "warranty"
    _description = "Warranty Management"

    name = fields.Char(required=True)
    duration = fields.Integer(required=True, string="Duration (in years)")
    percentage = fields.Float(percentage=True, required=True)
    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        domain="[('name', 'like', 'warranty')]",
    )

    _sql_constraints = [
        ("duration_check", "CHECK(duration > 0)", "Duration must be greater than 0"),
        (
            "percentage_check",
            "CHECK(percentage >= 0 AND percentage <= 100)",
            "Percentage must be between 0 and 100",
        ),
    ]

    def name_get(self):
        """Override the name_get method to include the duration with 'years' in the name."""
        result = []
        for warranty in self:
            display_name = f"{warranty.duration} year"
            result.append((warranty.id, display_name))
        return result
