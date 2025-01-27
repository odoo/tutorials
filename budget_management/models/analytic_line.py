from odoo import fields, models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one(
        "budget.budget.line", "Budget Line", ondelete="cascade"
    )
