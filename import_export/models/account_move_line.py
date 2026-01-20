from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    custom_duty_charges = fields.Monetary()
    boe_tax_id = fields.Many2one(comodel_name="account.tax")
