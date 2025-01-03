from odoo import Command, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class BudgetWizard(models.TransientModel):
    _name = "budget.wizard"
    _description = "Budget Wizard"

    date_from = fields.Date(required=True, string="Start Date")
    date_to = fields.Date(
        string="Expiration Date",
        required=True,
        index=True,
    )
    periods = fields.Selection(
        selection=[("monthly", "Monthly"), ("quarterly", "Quarterly")],
        required=True,
        default="monthly",
    )
    analytic_account_ids = fields.Many2many("account.analytic.plan")

    def action_add_budget(self):
        if self.date_from >= self.date_to:
            raise ValidationError("Starting date must be before the ending date.")

        budgets_to_create = []
        budget_lines = []
        current_date = self.date_from

        while current_date <= self.date_to:
            if self.periods == "monthly":
                next_date = current_date + relativedelta(months=1, day=1, days=-1)
            elif self.periods == "quarterly":
                next_date = current_date + relativedelta(months=3, day=1, days=-1)

            period_end_date = min(next_date, self.date_to)

            for plan in self.analytic_account_ids:
                for account in plan.account_ids:
                    budget_lines.append(
                        Command.create(
                            {
                                "analytic_account_id": account.id,
                                "planned_amount": 0.0,
                                "practical_amount": 0.0,
                            }
                        )
                    )
            budgets_to_create.append(
                {
                    "date_from": current_date,
                    "date_to": period_end_date,
                    "budget_line_ids": budget_lines,
                }
            )
            current_date = period_end_date + relativedelta(days=1)

        for budget_data in budgets_to_create:
            self.env["budget.budget"].create(budget_data)
