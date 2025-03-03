from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_deposit = fields.Boolean(string="Requires Deposit")
    deposit_amount = fields.Monetary(
        string="Deposit Amount", 
        currency_field="currency_id",
        default=0.0,
    )

