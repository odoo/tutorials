from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    modular_type_ids = fields.Many2many(comodel_name='sale.mrp.modular', string='Modular Types')
