from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    modular_type_ids = fields.Many2many(
        string='Module Types', comodel_name='product.modular.type'
    )
