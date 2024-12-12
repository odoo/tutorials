from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
   
    @api.model_create_multi
    def create(self, vals_list):
        # print("* " * 100)
        # print(vals_list)
        # print("* " * 100)
        
        for vals in vals_list:
            entry_date = vals.get("date")
            if not entry_date:
                raise ValidationError("The date field is required to determine the appropriate budget.")
            
            budget_line = self.env["budget.management.budget.lines"].search([
                ("budget_id.date_start", "<=", entry_date),
                ("budget_id.date_end", ">=", entry_date),
                ("budget_id.active", "=", True),
                ("analytic_account_id", "=", vals.get("account_id"))
            ], limit=1)

            if budget_line:
                budget = budget_line.budget_id

                analytic_account_lines = self.env["account.analytic.line"].search_read(
                    [
                        ("account_id", "=", vals.get("account_id")),
                        ("date", ">=", budget.date_start),
                        ("date", "<=", budget.date_end),
                        ("amount", "<", 0),
                    ],
                    fields=["amount"],
                )
                # print(list(line.get("amount") for line in analytic_account_lines))
                achieved = (sum(line.get("amount") for line in analytic_account_lines))
                # print(budget.on_over_budget, abs(achieved + vals.get("amount")), budget_line.budget_amount)

                if budget.on_over_budget == "restriction":
                    if abs(achieved + vals.get("amount")) > budget_line.budget_amount:
                        raise ValidationError(
                            "You cannot create a budget line because it exceeds the allowed budget!"
                        )
        return super(AccountAnalyticLine, self).create(vals_list)

    def write(self, vals):
        if "date" in vals or "amount" in vals or "account_id" in vals:
            for record in self:
                entry_date = vals.get("date", record.date)

                budget_line = self.env["budget.management.budget.lines"].search([
                    ("budget_id.date_start", "<=", entry_date),
                    ("budget_id.date_end", ">=", entry_date),
                    ("budget_id.active", "=", True),
                    ("analytic_account_id", "=", vals.get("account_id", record.account_id.id))
                ], limit=1)

                if budget_line:
                    budget = budget_line.budget_id

                    analytic_account_lines = self.env["account.analytic.line"].search_read(
                        [
                            ("account_id", "=", vals.get("account_id", record.account_id.id)),
                            ("date", ">=", budget.date_start),
                            ("date", "<=", budget.date_end),
                            ("amount", "<", 0),
                        ],
                        fields=["amount"],
                    )
                    achieved = (sum(line.get("amount") for line in analytic_account_lines))

                    new_amount = vals.get("amount", record.amount)
                    if budget.on_over_budget == "restriction":
                        if abs(achieved - record.amount + new_amount) > budget_line.budget_amount:
                            raise ValidationError(
                                "You cannot modify the budget line because it exceeds the allowed budget!"
                            )

        return super(AccountAnalyticLine, self).write(vals)
