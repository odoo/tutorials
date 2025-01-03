from odoo import fields, models, Command
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class MultipleBudgetsWizard(models.Model):
    _name = "multiple.budgets.wizard"
    _description = "Add Multiple Budget at once"

    starting_date = fields.Date(string="Starting Date", required=True)
    ending_date = fields.Date(string="Ending Date", required=True)
    periods = fields.Selection(
        [
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
        ],
        default="monthly",
        required=True,
    )
    analytic_account_plan_ids = fields.Many2many(comodel_name="account.analytic.plan")

    def action_create_monthly_budgets(self):
        if self.starting_date >= self.ending_date:
            raise ValidationError("Starting date must be before the ending date.")

        budgets_to_create = []
        budget_lines = []
        current_date = self.starting_date

        while current_date <= self.ending_date:
            if self.periods == "monthly":
                next_date = current_date + relativedelta(months=1, day=1, days=-1)
            elif self.periods == "quarterly":
                next_date = current_date + relativedelta(months=3, day=1, days=-1)

            period_end_date = min(next_date, self.ending_date)

            for plan in self.analytic_account_plan_ids:
                for account in plan.account_ids:
                    budget_lines.append(
                        Command.create(
                            {
                                "analytic_account_id": account.id,
                                "budget_amount": 0.0,
                                "achieved_amount": 0.0,
                            }
                        )
                    )
            budgets_to_create.append(
                {
                    "period_start": current_date,
                    "period_end": period_end_date,
                    "budget_line_ids": budget_lines,
                }
            )
            current_date = period_end_date + relativedelta(days=1)

        for budget_data in budgets_to_create:
            self.env["budget.budget"].create(budget_data)
