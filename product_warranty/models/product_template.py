from odoo import api, fields, models

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    has_warranty = fields.Boolean(default=False)
    warranty_id = fields.Many2one('product.warranty', string="Warranty")
