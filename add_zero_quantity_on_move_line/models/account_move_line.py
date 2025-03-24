from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_zero_quantity = fields.Boolean(string="Is product quantity zero", help="if it is checked, product quanity will be zero")
