from odoo import api, models, fields
import random


class BudgetLine(models.Model):
    _name = "budget.budget.line"

    budget_id = fields.Many2one(
        string="Budget",
        comodel_name="budget.budget",
        default=lambda self: self.env.context.get("active_id"),
        ondelete="cascade",
    )
    state = fields.Selection(related='budget_id.state')
    budget_amount = fields.Monetary(
        string="Budget Amount",
        required=True,
        help="Filled from Account Analytics Line",
        currency_field="currency_id",
    )
    achieved_amount = fields.Monetary(
        string="Achieved Amount",
        compute="_compute_achieved_amount",
        default=0,
        currency_field="currency_id",
        store=True,
    )
    achieved_percentage = fields.Integer(
        string="Achived(%)",
        compute="_compute_achieved_percentage",
        default=0,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="budget_id.company_id",
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        readonly=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account", comodel_name="account.analytic.account"
    )
    name = fields.Char(
        related="analytic_account_id.name"
    )  # to show the name of the account in gantt view

    account_analytics_line_ids = fields.One2many(
        string="Account analytics line id",
        comodel_name="account.analytic.line",
        inverse_name="budget_line_id",
        ondelete="cascade",
        readonly=True
    )
    date_start = fields.Date(
        string="Start Date", related="budget_id.date_start", store=True
    )
    date_end = fields.Date(string="End Date", related="budget_id.date_end", store=True)
    color = fields.Integer(
        string="color", compute="_compute_line_color_code", store=True
    )

    @api.depends('budget_id')
    def _compute_line_color_code(self):
        for record in self:
            record.color = random.choice(range(1, 12))

    @api.depends("budget_amount", "achieved_amount")
    def _compute_achieved_percentage(self):
        for line in self:
            line.achieved_percentage = (
                line.budget_amount and (line.achieved_amount / line.budget_amount) * 100
            )

    @api.depends("account_analytics_line_ids.amount")
    def _compute_achieved_amount(self):
        for record in self:
            account_analytics_line_ids_sum = 0
            for line in record.account_analytics_line_ids:
                if line.amount < 0:
                    account_analytics_line_ids_sum += line.amount

            record.achieved_amount = abs(account_analytics_line_ids_sum)

    def action_open_budget_line(self):
        return {
            "type": "ir.actions.act_window",
            "name": "analytics line",
            "res_model": "account.analytic.line",
            "view_mode": "list",
            "context": {
                "default_budget_id": self.budget_id.id,
                "default_account_id": self.analytic_account_id.id,
            },
            "domain": [
                ("budget_id", "=", (self.budget_id.id)),
                ("account_id", "in", self.analytic_account_id.ids),
                ("amount", "<", 0)
            ],
        }
