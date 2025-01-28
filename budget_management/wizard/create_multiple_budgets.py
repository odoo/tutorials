from dateutil.relativedelta import relativedelta
from odoo import models, fields

def date_range(start_date, end_date, step):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += step

class CreateMultipleBudgets(models.TransientModel):
    _name = "create.multiple.budgets"
    _description = "Create Multiple Budgets"

    starting_date = fields.Date("Start Date", required=True)
    ending_date = fields.Date("End Date", required=True)
    periods = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly')
    ], required=True)
    
    analytic_accounts = fields.Many2many('account.analytic.account', string="Analytic Accounts")

    def action_create_budgets(self):
        """Create budgets based on the selected period and date range."""
        if self.starting_date > self.ending_date:
            raise ValueError("Start date must be before end date.")

        step = relativedelta(months=1) if self.periods == "monthly" else relativedelta(months=3)

        budgets = []
        for date_from in date_range(self.starting_date, self.ending_date, step):
            date_to = date_from + step - relativedelta(days=1)
            if date_to > self.ending_date:
                break

            budget_lines = [
                (0, 0, {"analytics_account": analytic_account.id, "budget_amount": 0.0}) for analytic_account in self.analytic_accounts
            ]

            budgets.append({
                "starting_date": date_from,
                "ending_date": date_to,
                "budget_line_ids": budget_lines,
            })

        self.env["budget.budget"].create(budgets)
