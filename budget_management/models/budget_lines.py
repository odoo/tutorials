from odoo import api, fields, models


class BudgetBudget(models.Model):
    _name = "budget.line"
    _description = "Budget Lines"

    analytic_account = fields.Many2one("account.analytic.account")
    budget_amount = fields.Integer("Budget Amount", required=True)
    achieved_amount = fields.Integer("Achieved Amount")
    budget_id = fields.Many2one("budget.budget")
    progress = fields.Float("Achieved (%)")

    def related_account_analytic_lines():
        return 1
