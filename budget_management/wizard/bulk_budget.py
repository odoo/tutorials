from dateutil.relativedelta import relativedelta
from odoo import _, fields, models
from odoo.tools import date_utils


class CreateBulkBudgets(models.TransientModel):
    _name = "bulk.budget"
    _description = "Create Bulk Budgets"

    date_from = fields.Date("Start Date", required=True)
    date_to = fields.Date("End Date", required=True)
    periods = fields.Selection(
        string="Periods",
        selection=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
        ],
        required=True,
    )
    analytical_account_ids = fields.Many2many(
        "account.analytic.account", string="Analytic Plans", required=True
    )
    budget_amount = fields.Integer()

    def action_bulk_budgets(self):
        if self.periods == "monthly":
            step = relativedelta(months=1)
        elif self.periods == "quarterly":
            step = relativedelta(months=3)

        budgets = []
        budget_count = 1
        for date_from in date_utils.date_range(self.date_from, self.date_to, step):
            date_to = date_from + step - relativedelta(days=1)
            if date_to > self.date_to:
                break

            budget_lines = []
            for record in self.analytical_account_ids:
                line_name = f"Budget Line {budget_count}"
                budget_lines.append(
                    (
                        0,
                        0,
                        {
                            "name": line_name,
                            "analytic_account": record.id,
                            "budget_amount": self.budget_amount,
                        },
                    )
                )
                budget_count += 1

            budgets.append(
                {
                    "name": f"Budget {date_from.strftime('%Y-%m-%d')} to {date_to.strftime('%Y-%m-%d')}",
                    "date_from": date_from,
                    "date_to": date_to,
                    "budget_line_ids": budget_lines,
                }
            )

        self.env["budget.budget"].create(budgets)

        return {
            "name": _("Budgets"),
            "view_mode": "kanban",
            "res_model": "budget.budget",
            "type": "ir.actions.act_window",
        }
