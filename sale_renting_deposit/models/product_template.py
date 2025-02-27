from odoo import fields, models, api
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposit = fields.Boolean(string="Require Deposit")
    deposit_product_amount = fields.Float(string="Amount")
