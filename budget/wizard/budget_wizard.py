from odoo import models, fields,Command
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
    analytical_plan_ids = fields.Many2many("account.analytic.plan", string="Analytic Accounts")

    def action_add_budget(self):
        if self.date_from >= self.date_to:
            raise ValidationError("Start Date must be before Expiration Date.")

        current_date = self.date_from
        budget_entries = []

        while current_date <= self.date_to:
            
            end_of_month = current_date + relativedelta(day=31)

            
            if end_of_month > self.date_to:
                end_of_month = self.date_to
                
            
            budget_entry = {
                "name": f"Budget from {current_date.strftime('%d-%m-%Y')} to {end_of_month.strftime('%d-%m-%Y')}",
                "date_from": current_date,
                "date_to": end_of_month,
                "budget_lines": [],
            }

            for analytic_account in self.analytic_account_ids:
                budget_entry["budget_lines"].append(
                    Command.create({
                        "analytic_account_id": analytic_account.id,
                    })
                )
            budget_entries.append(budget_entry)

            
            current_date = end_of_month + timedelta(days=1)

            if current_date > self.date_to:
                break

        self.env["budget.budget"].create(budget_entries)

        return {"type": "ir.actions.act_window_close"}