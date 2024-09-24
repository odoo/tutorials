from odoo import models, fields, api


class WarrantyConfiguration(models.Model):
    _name='warranty.configuration'
    
    name = fields.Char()
    product_id = fields.Many2one('product.template',string="product")
    period = fields.Integer('Period')
    percentage = fields.Float()