from odoo import fields, models


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    require_deposite = fields.Boolean(string="Requires Deposite?")
    deposite_amount = fields.Monetary(string="Deposite Amount")
