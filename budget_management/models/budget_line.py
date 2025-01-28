from odoo import models, fields, api

class BudgetLine(models.Model):
    _name = 'budget.line'
    _description = 'A Budget Line'

    name = fields.Char("Name", default=lambda self: f"Budget Line {self.env['budget.line'].search_count([]) + 1}")

    budget_id = fields.Many2one('budget.budget', 'Budget')
    analytics_account = fields.Many2one('account.analytic.account', string='Analytics Account')
    
    budget_amount = fields.Float('Budget Amount')
    achieved_amount = fields.Float('Achieved Amount', compute='_compute_achieved_amount', store=True)
    over_budget = fields.Float('Over Budget', compute='_compute_over_budget', store=True)
    achieved_amount_percentage = fields.Float('Achieved (%)', compute="_compute_achieved_amount_percentage")
    
    account_analytic_lines = fields.One2many('account.analytic.line', "budget_line")
    responsible_person = fields.Many2one(related='budget_id.responsible_person')
    starting_date = fields.Date(related='budget_id.starting_date')
    ending_date = fields.Date(related='budget_id.ending_date')

    @api.depends('budget_amount', 'achieved_amount')
    def _compute_achieved_amount_percentage(self):
        for record in self:
            if record.budget_amount:
                record.achieved_amount_percentage = record.achieved_amount * 100 / record.budget_amount
            else:
                record.achieved_amount_percentage = 0

    @api.depends('budget_amount', 'achieved_amount')
    def _compute_over_budget(self):
        for record in self:
            if record.achieved_amount > record.budget_amount:
                record.over_budget = record.achieved_amount - record.budget_amount
            else:
                record.over_budget = 0

    def action_view_analytic_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Analytic Account Lines',
            'res_model': 'account.analytic.line',
            'view_mode': 'list',
            'domain': [('budget_line', '=', self.id)],
            'context': {
                'default_account_id': self.analytics_account.id,
                'default_budget_line': self.id,
            },
            'target': 'current',
        }
    
    @api.depends("analytics_account")
    def _compute_achieved_amount(self):
        for record in self:
            analytic_lines = self.env["account.analytic.line"].search(
                [
                    ("amount", "<", 0),
                    ("date", ">=", record.budget_id.starting_date),
                    ("date", "<=", record.budget_id.ending_date),
                    ("account_id", "=", record.analytics_account.id),
                ]
            )
            achieved_total = sum(analytic_lines.mapped("amount"))
            record.write({ 'achieved_amount': abs(achieved_total) })
