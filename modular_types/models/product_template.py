from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    modular_types = fields.Many2many('modular.type')
