from odoo import fields, models

class AccountAnalyticalLine(models.Model):
    _inherit = 'account.analytic.line'

    budget_line_id = fields.Many2one('budget.line', ondelete='cascade')
