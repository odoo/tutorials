from odoo import models, fields, api

class BudgetLine(models.Model):
    _name = "budget.management.budget.lines"

    name = fields.Char()
    budget_id = fields.Many2one("budget.budget", string="Budget")
    budget_amount = fields.Float(default=0.0)
    achieved_amount = fields.Float(default=0.0)
    achieved_percentage = fields.Float(
        default=0.0, 
        compute="_compute_achieved_percentage", 
        store=True
    )
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    # analytic_line_ids = fields.One2many('account.analytic.line', string='Analytic Account')
    date_start = fields.Date(string="Start Date", required=True)  
    date_end = fields.Date(string="End Date", required=False) 
        
    @api.depends("budget_amount", "achieved_amount")
    def _compute_achieved_percentage(self):
        for record in self:
            if record.budget_amount:
                record.achieved_percentage = (record.achieved_amount / record.budget_amount) * 100
            else:
                record.achieved_percentage = 0.0

