from odoo import fields, models


class ProductTemplate(models.Model):
    ''' Add field modular_types m2m for store Modular Types of products '''
    _inherit = 'product.template'

    modular_types = fields.Many2many('modular.type')
