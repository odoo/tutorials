from odoo import models, api, fields
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one(
        comodel_name="budget.budget.line",
        string="Budget line",
        compute="_compute_line_id",
        store=True,
        ondelete="cascade",
    )
    budget_id = fields.Many2one(comodel_name="budget.budget", string="Budget")

    @api.depends("budget_id")
    def _compute_line_id(self):
        for record in self:
            for line in record.budget_id.budget_line_ids:
                if record.account_id.id == line.analytic_account_id.id:
                    record.budget_line_id = line.id

    # budget_id on over budget warning need to be set
    @api.model
    def create(self, vals):
        budget = self.env["budget.budget"].browse(vals.get("budget_id"))
        line_account=[]

        for line in budget.budget_line_ids:
            line_account.append(line.analytic_account_id.id)
            if line.analytic_account_id.id == vals.get("account_id"):
                if abs(line.achieved_amount + vals.get("amount")) > line.budget_amount:
                    if budget.on_over_budget_type == "restriction_on_creation":
                        raise ValidationError(
                            f"amount can't be more than the budget amount ie., {line.budget_amount}"
                        )
        if(vals.get('account_id') not in line_account):
            raise ValidationError(f"Account {vals.get('account_id')} does't exists in the budget: {budget.name}")
        return super(AccountAnalyticLine, self).create(vals)
