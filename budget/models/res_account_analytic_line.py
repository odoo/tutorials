from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one('budget.budget.lines', 'Budget Line')
    # account_id = fields.Many2one('account.analytic.account', 'Automatic Account', related='budget_line_id.analytic_account_id.auto_account_id')

   
    
