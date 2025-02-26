from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Warranty of products"

    name = fields.Char("Name", required=True)
    product_template_id = fields.Many2one("product.template", string="Product", ondelete="cascade", required=True)
    percentage = fields.Float("Percentage")
    year = fields.Float("Year", digits=(3, 1))

    _sql_constraints = [
        ("unique_warranty_name", "unique(name)", "The Warranty Name must be unique.")
    ]

    @api.constrains("year")
    def _constrains_year(self):
        for record in self:
            if record.year > 10.0:
                raise ValidationError("Year must be less than 10")
