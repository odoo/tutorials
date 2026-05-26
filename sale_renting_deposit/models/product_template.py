from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_deposit_required = fields.Boolean(default=False)
    deposit_amount = fields.Float()
