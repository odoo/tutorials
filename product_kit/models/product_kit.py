from odoo import models, fields, api

class EstateKit(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string="Is Kit")
    sub_products_kit_ids = fields.Many2many("product.product" )
