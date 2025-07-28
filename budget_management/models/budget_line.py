from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class BudgetLine(models.Model):
    _name = "budget.management.budget.lines"
    _description = "Budget Management Budget Lines"

    name = fields.Char(string="Name")
    budget_id = fields.Many2one(
        comodel_name="budget.budget", string="Budget", required=True, ondelete="cascade"
    )
    state = fields.Selection(related="budget_id.state", readonly=True)
    budget_amount = fields.Monetary(
        string="Budget Amount",
        default=0.0,
        currency_field="currency_id",
        help="The total allocated budget for this budget line.",
    )
    achieved_amount = fields.Monetary(
        string="Achieved Amount",
        compute="_compute_achieved_amount",
        store=True,
        currency_field="currency_id",
    )
    achieved_percentage = fields.Float(
        string="Achieved (%)",
        compute="_compute_percentage_and_over_budget",
        store=True,
        readonly=True,
        help="Percentage of the budget achieved based on analytic lines.",
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account", required=True
    )
    over_budget = fields.Monetary(
        string="Over Budget",
        compute="_compute_percentage_and_over_budget",
        store=True,
        help="The amount by which the budget line exceeds its allocated budget.",
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="budget_id.currency_id",
        string="Currency",
        readonly=True,
    )

    count_analytic_lines = fields.Integer()
    start_date = fields.Date(related="budget_id.date_start")
    end_date = fields.Date(related="budget_id.date_end")
    user_id = fields.Many2one(related="budget_id.responsible")

    @api.depends("achieved_amount")
    def _compute_percentage_and_over_budget(self):
        # print("% " * 100)
        for record in self:
            if (
                record.analytic_account_id
                and record.budget_amount
                and record.achieved_amount
            ):
                record.achieved_percentage = (
                    (record.achieved_amount / record.budget_amount) * 100
                    if record.budget_amount > 0
                    else 0.0
                )
                record.over_budget = max(
                    0.0, record.achieved_amount - record.budget_amount
                )

    @api.depends("budget_amount")
    def _compute_achieved_amount(self):
        # print("+ " * 100)
        for record in self:
            if not record.analytic_account_id:
                record.achieved_amount = 0.0
                record.achieved_percentage = 0.0
                record.over_budget = 0.0
                continue
            analytic_account_lines = self.env["account.analytic.line"].search_read(
                [
                    ("auto_account_id", "=", record.analytic_account_id.id),
                    ("date", ">=", record.budget_id.date_start),
                    ("date", "<=", record.budget_id.date_end),
                    ("amount", "<", 0),
                ],
                fields=["amount"],
            )

            achieved = sum(line.get("amount") for line in analytic_account_lines)

            record.achieved_amount = abs(achieved)

    @api.constrains("budget_amount")
    def _check_budget_amount(self):
        for record in self:
            if record.budget_amount < 0:
                raise ValidationError("Budget amount cannot be negative.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("budget_id"):
                active_budget = self.env["budget.budget"].browse(vals["budget_id"])
                if active_budget.state != "draft":
                    raise UserError(
                        "Budget lines can only be created when the budget is in 'draft' state."
                    )

        return super(BudgetLine, self).create(vals_list)

    def open_analytic_lines_action(self):
        if not self.budget_id:
            raise UserError("No budget linked to this budget line.")

        budget_start_date = self.budget_id.date_start
        budget_end_date = self.budget_id.date_end

        return {
            "type": "ir.actions.act_window",
            "name": "Analytic Lines",
            "res_model": "account.analytic.line",
            "view_mode": "list",
            "target": "current",
            "context": {
                "default_account_id": self.analytic_account_id.id,
                "budget_start_date": budget_start_date,
                "budget_end_date": budget_end_date,
            },
            "domain": [
                ("account_id", "=", self.analytic_account_id.id),
                ("date", ">=", budget_start_date),
                ("date", "<=", budget_end_date),
                ("amount", "<", 0),
            ],
        }
