from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    deposit_status = fields.Boolean("Require Deposit")
    deposit_amount = fields.Float("Deposit Amount")
