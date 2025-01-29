from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "budget.line"

    name = fields.Char(default="budget line")
    budget_total = fields.Float()
    budget_achive = fields.Float(compute="_compute_achieved_amount", store=True)
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
    )
    budget_id = fields.Many2one("budget.budget", ondelete="cascade")
    date_from = fields.Date(related="budget_id.duration_start_date", store=True)
    date_to = fields.Date(related="budget_id.duration_end_date", store=True)
    analytic_line_ids = fields.One2many("account.analytic.line", "budget_line_id")

    @api.constrains("budget_achive")
    def _constrains_amount(self):
        for record in self:
            if record.budget_id.over_budget == "restriction":
                if record.budget_achive > record.budget_total:
                    raise ValidationError(
                        "Invalid amount! The achieved budget cannot exceed the total budget. Please adjust the amount accordingly."
                    )

    @api.depends("analytic_line_ids.amount")
    def _compute_achieved_amount(self):
        for line in self:
            line.budget_achive = abs(
                sum(
                    line.analytic_line_ids.filtered(lambda l: l.amount < 0).mapped(
                        "amount"
                    )
                )
            )

    def action_open_account_analytic(self):
        return {
            "name": "Analytic Lines",
            "view_mode": "list,form",
            "res_model": "account.analytic.line",
            "type": "ir.actions.act_window",
            "context": {
                "default_budget_line_id": self.id,
                "default_account_id": self.analytic_account_id.id,
                "default_date": self.budget_id.duration_start_date,
            },
            "domain": [("budget_line_id", "=", self.id)],
        }
