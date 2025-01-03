from odoo import fields, models
from dateutil.relativedelta import relativedelta


class MultipleBudgetWizard(models.TransientModel):
    _name = "multiple.budget.wizard"
    _description = "Multiple Budget Wizard"

    duration_start_date = fields.Date(string="Duration")
    duration_end_date = fields.Date(string="->")
    periods = fields.Selection(
        string="Periods",
        selection=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
        ],
    )
    analytical_plan_ids = fields.Many2many("account.analytic.plan", string="Analytic Accounts")

    def action_budget_split(self):
        budgets = []
        if self.periods == "monthly":
            current_date = self.duration_start_date
            while current_date <= self.duration_end_date:
                end_date = current_date + relativedelta(months=1, days=-1)
                if end_date > self.duration_end_date:
                    end_date = self.duration_end_date
                budgets.append(self.env['budget.budget'].create({
                    'period_start_date': current_date,
                    'period_end_date': end_date,
                    'analytical_plan_ids': self.analytical_plan_ids,
                }))
                current_date += relativedelta(months=1)
        elif self.periods == "quarterly":
            current_date = self.duration_start_date
            while current_date <= self.duration_end_date:
                end_date = current_date + relativedelta(months=3, days=-1)
                if end_date > self.duration_end_date:
                    end_date = self.duration_end_date
                budgets.append(self.env['budget.budget'].create({
                    'period_start_date': current_date,
                    'period_end_date': end_date,
                    'analytical_plan_ids': self.analytical_plan_ids,
                }))
                current_date += relativedelta(months=3)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'budget.budget',
            'view_mode': 'kanban,form',
            'domain': [('id', 'in', [b.id for b in budgets])],
            'name': 'Budgets',
        }
