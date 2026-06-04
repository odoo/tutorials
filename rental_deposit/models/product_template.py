from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_deposit = fields.Boolean()
    deposit_amount = fields.Float()
