from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class BudgetLines(models.Model):
    _name = "budget.lines"
    _description = "Budget Line"

    budget_id = fields.Many2one(
        "budget.budget", "Budget", ondelete="cascade", index=True, required=True
    )
    state = fields.Selection(related="budget_id.state", readonly=True)
    analytic_account_id = fields.Many2one(
        "account.analytic.account", "Analytic Account"
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    planned_amount = fields.Monetary(
        "Budget Amount",
        required=True,
        default=0.0,
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.",
    )
    practical_amount = fields.Monetary(
        string="Achieved Amount",
        compute="_compute_practical_amount",
        default=0.0,
    )
    percentage = fields.Float(
        default=0.0,
        help="Comparison between practical and planned amount. This measure tells you if you are below or over budget.",
    )
    date_start = fields.Date(
        string="Start Date", related="budget_id.date_from", store=True
    )
    end_date = fields.Date(string="End Date", related="budget_id.date_to", store=True)
    company_id = fields.Many2one(
        "res.company", related="budget_id.company_id", string="Company", store=True
    )
    over_budget = fields.Monetary(
        string="Over Budget",
        default=0.0,
        compute="_compute_practical_amount",
        help="The amount by which the budget line exceeds its allocated budget.",
    )

    @api.constrains("practical_amount", "planned_amount")
    def _check_restriction_on_creation(self):
        for record in self:
            if record.budget_id.on_over_budget == "restriction on creation":
                if record.practical_amount > record.planned_amount:
                    raise ValidationError(
                        "Practical amount cannot exceed planned amount when 'Restriction On Creation' is selected."
                    )

    @api.constrains("planned_amount")
    def _check_planned_amount(self):
        for record in self:
            if record.planned_amount < 0:
                raise ValidationError("Budget amount cannot be negative.")

    @api.depends("analytic_account_id", "budget_id.date_from", "budget_id.date_to")
    def _compute_practical_amount(self):
        for record in self:
            if not record.analytic_account_id:
                record.practical_amount = 0.0
                record.over_budget = 0.0
                continue

            analytic_lines = self.env["account.analytic.line"].search(
                [
                    ("account_id", "=", record.analytic_account_id.id),
                    ("date", ">=", record.budget_id.date_from),
                    ("date", "<=", record.budget_id.date_to),
                    ("amount", "<", 0),
                ]
            )
            total_achieved = abs(sum(analytic_lines.mapped("amount")))
            record.practical_amount = total_achieved
            record.over_budget = max(0.0, total_achieved - record.planned_amount)

    def open_analytic_lines_action(self):
        """Open the analytic lines in a filtered list view."""
        if not self.analytic_account_id:
            raise UserError("Please set an Analytic Account for this budget line.")

        return {
            "type": "ir.actions.act_window",
            "name": "Analytic Lines",
            "res_model": "account.analytic.line",
            "view_mode": "list",
            "target": "current",
            "context": {
                "default_account_id": self.analytic_account_id.id,
                "default_date": self.budget_id.date_from,
            },
            "domain": [
                ("account_id", "=", self.analytic_account_id.id),
                ("date", ">=", self.budget_id.date_from),
                ("date", "<=", self.budget_id.date_to),
            ],
        }
