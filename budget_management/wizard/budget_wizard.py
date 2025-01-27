from dateutil.relativedelta import relativedelta

from odoo import Command, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


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
    analytic_account_ids = fields.Many2many(
        "account.analytic.account", string="Analytic Accounts"
    )

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if "date_from" in fields_list and not defaults.get("date_from"):
            defaults["date_from"] = date_utils.start_of(
                fields.Date.context_today(self), "year"
            )
        if "date_to" in fields_list and not defaults.get("date_to"):
            defaults["date_to"] = date_utils.end_of(
                fields.Date.context_today(self), "year"
            )
        return defaults

    def action_add_budget(self):
        if self.date_from >= self.date_to:
            raise ValidationError("The starting date must be before the ending date.")

        budgets_to_create = []
        current_date = self.date_from

        while current_date <= self.date_to:
            # Determine the end date for the period based on the selected period type
            if self.periods == "monthly":
                next_date = current_date + relativedelta(months=1, day=1, days=-1)
            elif self.periods == "quarterly":
                next_date = current_date + relativedelta(months=3, day=1, days=-1)
            else:
                raise ValidationError(
                    "Invalid period type. Please choose 'monthly' or 'quarterly'."
                )

            # Ensure the period does not extend beyond the overall end date
            period_end_date = min(next_date, self.date_to)

            # Create budget lines for each analytic account
            budget_lines = [
                Command.create(
                    {
                        "name": f"Budget for {account.name}",
                        "account_id": account.id,
                        "amount": 0.0,
                    }
                )
                for account in self.analytic_account_ids
            ]

            # Append the budget data for this period
            budgets_to_create.append(
                {
                    "date_from": current_date,
                    "date_to": period_end_date,
                    "budget_line_ids": budget_lines,
                }
            )

            # Move to the next period
            current_date = period_end_date + relativedelta(days=1)

        # Create all budgets in a batch
        self.env["budget.budget"].create(budgets_to_create)
