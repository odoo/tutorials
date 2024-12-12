from odoo import models, fields, Command
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class AddBudgetWizard(models.TransientModel):
    _name = "add.budget.wizard"
    _description = " "

    date_start = fields.Date(required=True, string="Start Date")
    date_end = fields.Date(
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
        "account.analytic.account", string="Analytic Account", required=True
    )

    def action_add_budget(self):
        """Creates budget records based on the selected periods."""
        if self.date_start >= self.date_end:
            raise ValueError("Start Date must be before Expiration Date.")

        current_date = self.date_start
        budget_entries = []

        while current_date <= self.date_end:
            next_date = (
                current_date + relativedelta(months=1)
                if self.periods == "monthly"
                else current_date + relativedelta(months=3)
            )
            end_date = min(next_date - timedelta(days=1), self.date_end)

            budget_entries.append(
                {
                    "name": (
                        f"Budget - {current_date.strftime('%B-%Y')}"
                        if self.periods == "monthly"
                        else f"Budget - {current_date.strftime('%d %B, %Y')} to {end_date.strftime('%d %B, %Y')}"
                    ),
                    "date_start": current_date,
                    "date_end": end_date,
                    "budget_line_ids": [
                        Command.create(
                            {"name": "budget line", "analytic_account_id": account.id}
                        )
                        for account in self.analytic_account_ids
                    ],
                }
            )

            current_date = next_date

        self.env["budget.budget"].create(budget_entries)

        return {
            "type": "ir.actions.client",
            "tag": "reload",
            "message": "Budgets have been successfully created.",
        }
