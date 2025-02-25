from odoo import  fields, models


class ProductWarrantyConfig(models.Model):
    _name = 'product.warranty.config'
    _description = 'Product Warranty Config'

    name = fields.Char(string='Name', required=True)
    product_template_id = fields.Many2one(comodel_name='product.template', string='Product', required=True)
    percentage = fields.Float(string='Percentage', required=True)
    years = fields.Integer(string='Years', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique!'),
    ]
