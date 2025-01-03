from odoo import api, fields, models
from odoo.exceptions import UserError


class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget Line"

    name = fields.Char(string="Name", related="budget_analytic_id.name")
    budget_id = fields.Many2one("budget.budget", "Budget", ondelete="cascade")
    budget_analytic_id = fields.Many2one("account.analytic.account", "Analytic Account")
    analytic_line_ids = fields.One2many(
        "account.analytic.line", "budget_line_id", string="Analytic Lines"
    )
    budget_amount = fields.Monetary(
        string="Budget Amount", currency_field="currency_id"
    )
    achieved_amount = fields.Monetary(
        string="Achieved Amount",
        currency_field="currency_id",
        compute="_compute_achieved_amount",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id.id
    )
    is_above_budget = fields.Boolean(compute="_compute_all", store=True)
    achieved_percentage = fields.Float(compute="_compute_all", store=True)
    start_date = fields.Date(related="budget_id.date_from")
    end_date = fields.Date(related="budget_id.date_to")
    user_id = fields.Many2one(related="budget_id.user_id")
    over_budget_amount = fields.Monetary(
        compute="_compute_all", store=True, currency_field="currency_id"
    )

    @api.constrains("budget_analytic_id", "budget_id")
    def _check_analytic_account_not_is_above_budget(self):
        for record in self:
            existing = any(
                line.budget_analytic_id == record.budget_analytic_id
                and line.is_above_budget
                for line in record.budget_id.budget_line_ids
            )
            if existing and record.budget_id.on_over_budget == "restrict":
                raise UserError(
                    "You cannot create a budget line with an analytic account that is already over budget."
                )

    @api.depends("analytic_line_ids")
    def _compute_achieved_amount(self):
        for record in self:
            record.achieved_amount = sum(
                line.amount for line in record.analytic_line_ids
            )

    @api.depends("achieved_amount", "budget_amount")
    def _compute_all(self):
        for record in self:
            record.is_above_budget = record.achieved_amount > record.budget_amount
            record.over_budget_amount = max(
                0, record.achieved_amount - record.budget_amount
            )
            record.achieved_percentage = (
                record.budget_amount
                and (record.achieved_amount / record.budget_amount) * 100
            )

    def open_analytic_account(self):
        return {
            "name": "Analytic Account",
            "type": "ir.actions.act_window",
            "res_model": "budget.line",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }
