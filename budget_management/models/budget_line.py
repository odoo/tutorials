from odoo import fields, models, api


class BudgetLine(models.Model):
    _name = 'budget.line'
    _description = "Budget Line Table"

    name = fields.Char()
    analytic_account_id = fields.Many2one('account.analytic.account')
    period_start_date = fields.Date("Start Date", related="budget_id.period_start_date")
    period_end_date = fields.Date("End Date", related="budget_id.period_end_date")
    budget_amount = fields.Float()
    archived_amount = fields.Float(compute="_calculate_amount")
    budget_id = fields.Many2one('budget.budget', ondelete="cascade")
    account_analytic_line_ids = fields.One2many('account.analytic.line', 'budget_line_id')
    progress_percentage = fields.Float(string='Progress', compute='_compute_progress_percentage')


    @api.depends('archived_amount', 'budget_amount')
    def _compute_progress_percentage(self):     # Compute Method : Percentage of the progressbar
        for record in self:
            if record.budget_amount > 0:
                record.progress_percentage = (record.archived_amount / record.budget_amount) * 100
            else:
                record.progress_percentage = 0


    @api.depends('analytic_account_id')
    def _calculate_amount(self):                # Compute Method : Calculatation of Archive Amount
        for record in self:
            linked_lines = self.env["account.analytic.line"].search(
                [
                    ("amount", "<", 0),
                    ("date", ">=", record.period_start_date),
                    ("date", "<=", record.period_end_date),
                    ("account_id", "=", record.analytic_account_id.id),
                ]
            )
            achieved_sum = sum(linked_lines.mapped("amount"))
            record.write({
                'archived_amount': abs(achieved_sum)
            })

    def action_open_budget_entries(self):      # Action Button : Open Form view of account.analytic.line
        return {
            "type": "ir.actions.act_window",
            "name": "Analytical Lines",
            "res_model": "account.analytic.line",
            "target": "current",
            "view_mode": "list",
            "res_id": self.id,
            "domain": [
                ("account_id", "=", self.analytic_account_id.id),
                ("date", ">=", self.period_start_date),
                ("date", "<=", self.period_end_date),
            ],
        }
