from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget Line"

    analytic_account_ids = fields.One2many("account.analytic.line", "budget_line_id", string="Analytic Account")
    budget_amount = fields.Integer(string="Budget Amount")
    achieved_amount = fields.Integer(string="Achieved Amount", compute="_compute_achieved_amount")
    achieved_percentage = fields.Integer(string="Achieved(%)", compute="_compute_achieved_percentage")
    budget_id = fields.Many2one("budget.budget", string="Budget")
    period_start_date = fields.Date(related="budget_id.period_start_date")
    period_end_date = fields.Date(related="budget_id.period_end_date")
    on_over_budget = fields.Selection(related="budget_id.on_over_budget")


    @api.constrains("budget_amount", "achieved_amount")
    def _check_budget_amount(self):
            for line in self:
                if line.achieved_amount > line.budget_amount and line.budget_id.on_over_budget == "restriction":
                    raise ValidationError("not allowed to create accont analytic line")
    @api.depends("achieved_amount", "budget_amount")
    def _compute_achieved_percentage(self):
        for line in self:
            line.achieved_percentage = line.budget_amount and 100*line.achieved_amount / line.budget_amount


    @api.depends("analytic_account_ids")
    def _compute_achieved_amount(self):
        for line in self:
            total_achieved_amount = sum(
                self.env['account.analytic.line'].search([
                    ('account_id', '=', line.analytic_account_ids.id)
                ]).mapped('amount')
            )
            line.achieved_amount = total_achieved_amount
        
    
    def open_account_analytic_view(self):
        return {    
            "type": "ir.actions.act_window",
            "res_model": "account.analytic.line",
            "view_mode": "form",
            "name": "Budget",
            "target": "main",
        }