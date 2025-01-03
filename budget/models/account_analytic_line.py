from odoo import models, api, fields
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AccountAnalyticLine, self).create(vals_list)
        for vals in vals_list:
            self._update_budget_line(vals.get("account_id"), vals.get("date"))
        return records

    def write(self, vals):
        result = super(AccountAnalyticLine, self).write(vals)
        for record in self:
            account_id = vals.get("account_id", record.account_id.id)
            entry_date = vals.get("date", record.date)
            self._update_budget_line(account_id, entry_date)
        return result

    def _update_budget_line(self, analytic_account_id, entry_date):
        """Update the practical amount of the related budget line."""
        if not analytic_account_id or not entry_date:
            return

        budget_line = self.env["budget.lines"].search(
            [
                ("analytic_account_id", "=", analytic_account_id),
                ("budget_id.date_from", "<=", entry_date),
                ("budget_id.date_to", ">=", entry_date),
            ],
            limit=1,
        )

        if budget_line:
            budget_line._compute_practical_amount()
