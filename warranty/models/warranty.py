from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Warranty(models.Model):
    _name = "warranty"
    _description = "Warranty Configuration"

    name = fields.Char("Name", required=True)
    product_id = fields.Many2one("product.template", string="Product", required=True)
    percentage = fields.Float("Percentage", required=True)
    year = fields.Integer("Years", required=True, default=1)

    @api.constrains('product_id', 'year')
    def _check_unique_product_year(self):
        for record in self:
            if self.search_count([
                ('product_id', '=', record.product_id.id),
                ('year', '=', record.year),
                ('id', '!=', record.id)
            ]) > 0:
                raise ValidationError(_("A warranty configuration already exists for this product and year combination."))
