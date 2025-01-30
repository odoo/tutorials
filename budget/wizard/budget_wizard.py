from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import fields, models


class BudgetWizard(models.TransientModel):
    _name = "budget.wizard"
    _description = "budget.wizard"

    date_start = fields.Date()
    date_end = fields.Date()
    duration = fields.Selection(
        [("Monthly", "Monthly"), ("Quarterly", "Quarterly")], default="Monthly"
    )
    account_id = fields.Many2many(
        "account.analytic.account",
    )

    def action_create_budgets(self):
        if self.date_start > self.date_end:
            raise ValueError("Start date must be before end date.")
        step = relativedelta(months=1)
        date_start = date(self.date_start.year, self.date_start.month, 1)
        if self.duration == "Quarterly":
            step = relativedelta(months=3)
            if self.date_start.month % 3 == 2:
                date_start = date(
                    self.date_start.year,
                    self.date_start.month + 1,
                    1,
                )
            elif self.date_start.month % 3 == 0:
                date_start = date(
                    self.date_start.year,
                    self.date_start.month + 2,
                    1,
                )

        c = 1
        while date_start <= self.date_end:
            date_to = date_start + step - relativedelta(days=1)
            self.env["budget.budget"].create(
                {
                    "name": ("Budget " + str(c)),
                    "duration_start_date": date_start,
                    "duration_end_date": date_to,
                    "budget_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": (
                                    "Budget " + str(c) + " " + analytic_account.name
                                ),
                                "analytic_account_id": analytic_account.id,
                            },
                        )
                        for analytic_account in self.account_id
                    ],
                }
            )
            c += 1
            date_start = date_to + relativedelta(days=1)
