# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget Line"
    _inherit = "analytic.plan.fields.mixin"
    _order = "sequence, id"

    name = fields.Char(related="account_id.name", string="Budget Name")
    color = fields.Integer(related="budget_id.color", string="Budget Color")
    sequence = fields.Integer("Sequence", default=10)
    budget_id = fields.Many2one(
        "budget", "Budget", ondelete="cascade", index=True, required=True
    )
    date_from = fields.Date("Start Date", related="budget_id.date_from", store=True)
    date_to = fields.Date("End Date", related="budget_id.date_to", store=True)
    currency_id = fields.Many2one(
        "res.currency", related="company_id.currency_id", readonly=True
    )
    budget_amount = fields.Monetary(string="Budgeted")
    achieved_amount = fields.Monetary(
        string="Achieved",
        compute="_compute_achieved_amount",
        help="Amount Billed/Invoiced.",
        readonly=True,
        store=True
    )
    achieved_percentage = fields.Float(
        compute="_compute_percentage", string="Achieved (%)"
    )
    company_id = fields.Many2one(
        related="budget_id.company_id",
        comodel_name="res.company",
        string="Company",
        store=True,
        readonly=True,
    )
    is_above_budget = fields.Boolean(compute="_compute_above_budget")
    budget_analytic_state = fields.Selection(
        related="budget_id.state", string="Budget State", store=True, readonly=True
    )
    analytic_line_ids = fields.One2many(
        "account.analytic.line",
        "budget_line_id",
        string="Analytic Lines",
    )

    @api.constrains("budget_amount", "achieved_amount")
    def _check_budget_overflow(self):
        for line in self:
            if line.budget_id:
                isOver = any(
                    line.account_id.id == lines.account_id.id
                    and lines.is_above_budget
                    and line.id != lines.id
                    for lines in line.budget_id.budget_line_ids
                )
                if isOver and line.budget_id.on_over_budget == "restriction":
                    raise ValidationError("Budget is Over for this analytic account")

    @api.depends("analytic_line_ids")
    def _compute_achieved_amount(self):
        for line in self:
            line.achieved_amount = sum(
                an_line.amount
                for an_line in line.analytic_line_ids
                if line.date_from <= an_line.date <= line.date_to
            )

    @api.depends("achieved_amount", "budget_amount")
    def _compute_above_budget(self):
        for line in self:
            line.is_above_budget = line.achieved_amount > line.budget_amount

    def _compute_percentage(self):
        for line in self:
            line.achieved_percentage = (
                line.budget_amount and (line.achieved_amount / line.budget_amount) * 100
            )

    def action_open_budget_entries(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Analytical Lines",
            "res_model": "account.analytic.line",
            "target": "new",
            "view_mode": "list",
            "context": {
                "default_account_id": self.account_id.id,
                "default_budget_line_id": self.id,
            },
            "domain": [
                ("account_id", "=", self.account_id.id),
                ("budget_line_id", "=", self.id),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
            ],
        }
