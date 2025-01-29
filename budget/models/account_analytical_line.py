from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one("budget.line", required=True, ondelete="cascade")
