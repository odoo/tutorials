from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one(comodel_name="budget.management.budget.lines")

    @api.model_create_multi
    def create(self, vals_list):
        # print("* " * 100)
        # print(vals_list)
        # print("* " * 100)
        for vals in vals_list:
            budget_line = self.env["budget.management.budget.lines"].browse(
                vals.get("budget_line_id")
            )
            budget = budget_line.budget_id
            if budget.on_over_budget == "restriction":
                if sum(budget_line.analytic_line_ids.mapped("amount"))+vals.get("amount") > budget_line.budget_amount:
                    raise ValidationError(
                        "You cannot create a budget line because it exceeds the allowed budget!"
                    )
        return super(AccountAnalyticLine, self).create(vals_list)

    def write(self, vals):
        # print("* " * 100)
        # print(vals)
        # print("* " * 100)
        if "amount" in vals:
            for record in self:
                old_amount = record.amount
                new_amount = vals.get("amount")
                print(old_amount,new_amount)
                total_amount = sum(record.budget_line_id.analytic_line_ids.mapped("amount")) + new_amount - old_amount

                budget_line = record.budget_line_id
                budget = budget_line.budget_id
                if budget.on_over_budget == "restriction" and total_amount > budget_line.budget_amount:
                    raise ValidationError(
                        "You cannot update this budget line because it exceeds the allowed budget!"
                    )          
                                                          
        return super(AccountAnalyticLine, self).write(vals)
