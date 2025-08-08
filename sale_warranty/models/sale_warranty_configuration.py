from odoo import fields, models


class SaleStockWarrantyConfiguration(models.Model):
    _name = 'sale.warranty.configuration'
    _description = 'sale.warranty.configuration'

    name = fields.Text(string='Name')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    year = fields.Integer(string='Duration (in years)')
    percentage = fields.Float(string='Percentage')
