from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetLine(models.Model):
    _name = "budget.budget.line"
    _description = "Budget Budget Line"

    name = fields.Char("Description", default="Budget Line")
    amount = fields.Float("Budget Amount", required=True)
    achieved_amount = fields.Float(
        "Achieved Amount", compute="_compute_achieved_amount", store=True
    )
    achieved_percent = fields.Float("Achieved %", compute="_compute_achieved_percent")
    date_from = fields.Date(related="budget_id.date_from")
    date_to = fields.Date(related="budget_id.date_to")
    sequence = fields.Integer("Sequence", default=1)
    budget_id = fields.Many2one("budget.budget", required=True)
    account_id = fields.Many2one("account.analytic.account", "Account")
    user_id = fields.Many2one(related="budget_id.user_id")
    analytic_line_ids = fields.One2many(
        "account.analytic.line", "budget_line_id", string="Analytic Lines"
    )

    @api.constrains("achieved_amount", "amount")
    def _check_restriction_on_creation(self):
        for record in self:
            if record.budget_id.action_over_budget == "restrict":
                if record.achieved_amount > record.amount:
                    raise ValidationError(
                        "Achieved amount cannot exceed amount when 'Restriction' is selected."
                    )

    @api.depends("amount", "achieved_amount")
    def _compute_achieved_percent(self):
        for line in self:
            if line.account_id and line.amount:
                line.achieved_percent = (line.achieved_amount) / line.amount * 100
            else:
                line.achieved_percent = 0

    @api.depends(
        "analytic_line_ids.amount",
    )
    def _compute_achieved_amount(self):
        for record in self:
            total_achieved = abs(
                sum(
                    record.analytic_line_ids.filtered(lambda l: l.amount < 0).mapped(
                        "amount"
                    )
                )
            )
            record.achieved_amount = total_achieved

    def action_open_analytic_lines(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Analytic Lines",
            "res_model": "account.analytic.line",
            "view_mode": "list",
            "target": "new",
            "context": {
                "default_account_id": self.account_id.id,
                "default_date": self.budget_id.date_from,
                "default_budget_line_id": self.id,
            },
        }
