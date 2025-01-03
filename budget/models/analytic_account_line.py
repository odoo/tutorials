from odoo import fields, models


class AnalyticAccountLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one("budget.line", "Budget Line", ondelete="cascade")
