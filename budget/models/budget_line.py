from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class BudgetLine(models.Model):
    _name = "budget.management.budget.lines"
    _description = "Budget Management Budget Lines"

    name = fields.Char(string="Name")
    budget_id = fields.Many2one(
        comodel_name="budget.budget", string="Budget", required=True
    )
    state = fields.Selection(related="budget_id.state")
    budget_amount = fields.Monetary(
        string="Budget Amount",
        default=0.0,
        currency_field="currency_id",
        help="The total allocated budget for this budget line.",
    )
    achieved_amount = fields.Monetary(
        string="Achieved Amount",
        default=0.0,
        compute="_compute_achieved_amount",
        store=True,
        currency_field="currency_id",
    )
    achieved_percentage = fields.Float(
        string="Achieved (%)",
        compute="_compute_achieved_amount",
        store=True,
        readonly=True,
        help="Percentage of the budget achieved based on analytic lines.",
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account", required=True
    )
    analytic_line_ids = fields.One2many(
        comodel_name="account.analytic.line",
        inverse_name="budget_line_id",
        string="Analytic Lines",
    )
    over_budget = fields.Monetary(
        string="Over Budget",
        compute="_compute_achieved_amount",
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

    # Add these fields for the Gantt view
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)

    @api.depends("analytic_line_ids.amount")
    def _compute_achieved_amount(self):
        for record in self:
            record.achieved_amount = sum(record.analytic_line_ids.mapped("amount"))
            record.achieved_percentage = (
                (record.achieved_amount / record.budget_amount) * 100
                if record.budget_amount > 0
                else 0.0
            )
            record.over_budget = max(0.0, record.achieved_amount - record.budget_amount)

            if (
                record.budget_id.on_over_budget == "warning"
                and record.achieved_amount > record.budget_amount
            ):
                record.budget_id.warnings = "Achieved amount is more than your budget!"
            else:
                record.budget_id.warnings = False

    @api.constrains("budget_amount")
    def _check_budget_amount(self):
        for record in self:
            if record.budget_amount < 0:
                raise ValidationError("Budget amount cannot be negative.")

    @api.model_create_multi
    def create(self, vals_list):
        active_budget = None
        if self.env.context.get("active_id"):
            active_budget = self.env["budget.budget"].browse(self.env.context.get("active_id"))
            if active_budget.state != "draft":
                raise UserError("Budget lines can only be created when the state is 'draft'.")
        else:
            for vals in vals_list:
                budget_id = vals.get("budget_id")
                if budget_id:
                    active_budget = self.env["budget.budget"].browse(budget_id)
                    break

        if not active_budget:
            raise UserError("No budget found in context or record.")

        if active_budget.state != "draft":
            raise UserError("Budget lines can only be created when the state is 'draft'.")

        return super(BudgetLine, self).create(vals_list)
