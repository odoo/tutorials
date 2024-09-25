from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_warranty_available = fields.Boolean('Is Warranty Available')
