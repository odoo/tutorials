from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    date_reloaded = fields.Date(string="Reloaded Date")
