from odoo import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one('budget.line', 'Budget', ondelete='cascade')
