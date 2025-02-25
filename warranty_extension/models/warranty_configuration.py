from odoo import api, fields, models
from odoo.exceptions import ValidationError

class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _description = "Warranty Configuration"

    name = fields.Char(string="Warranty Name", required=True)
    product_template_id = fields.Many2one("product.template", string="Product", ondelete="cascade", required=True)
    year = fields.Float(string="Year", default=1)
    percentage = fields.Float(string="Percentage", required=True)

    sql_constraints = [
        ('name_uniq', 'unique(name)', 'A warranty with this name already exists!')
    ]
