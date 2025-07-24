from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    deposit_required = fields.Boolean(string="Require Deposit")
    deposit_amount = fields.Monetary(string="Amount")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
