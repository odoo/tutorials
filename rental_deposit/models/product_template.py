from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposite = fields.Boolean()
    amount = fields.Float()
