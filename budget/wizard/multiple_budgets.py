from dateutil.relativedelta import relativedelta
from odoo import Command, fields, models


class MultipleBudgets(models.TransientModel):
    _name = "multiple.budgets"
    _description = "Multiple Budgets"

    date_from = fields.Date()
    date_to = fields.Date()
    periods = fields.Selection(
        [("month", "Monthly"), ("quarter", "Quarterly")], default="month", required=True
    )
    analytic_account_plan_ids = fields.Many2many(
        "account.analytic.plan", string="Analytic Accounts"
    )

    def _get_dates(self):
        dates = []
        current_date = self.date_from
        end_date = self.date_to
        if self.periods == "month":
            period = 1
        elif self.periods == "quarter":
            period = 3
        while current_date < end_date:
            next_date = current_date + relativedelta(months=period)
            dates.append(
                (current_date, min(end_date, next_date - relativedelta(days=1)))
            )
            current_date = next_date
        return dates

    def create_multiple_budgets(self):
        dates = self._get_dates()
        for date_from, date_to in dates:
            self.env["budget.budget"].create(
                {
                    "date_from": date_from,
                    "date_to": date_to,
                    "budget_line_ids": [
                        Command.create(
                            {
                                "budget_analytic_id": line.id,
                            }
                        )
                        for line in self.analytic_account_plan_ids.account_ids
                    ],
                }
            )
