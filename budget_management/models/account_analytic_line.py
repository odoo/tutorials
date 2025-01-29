from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one(comodel_name="budget.line", string="Budget Line", ondelete="cascade" )
