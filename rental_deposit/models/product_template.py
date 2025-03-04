from odoo import models,fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_deposit = fields.Boolean(default=False, string="Require Deposit")
    amount = fields.Float(string="Amount")
    