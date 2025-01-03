from odoo import fields, models,api
from odoo.exceptions import ValidationError,UserError

class BudgetLines(models.Model):
    _name = "budget.budget.lines"
    _description = "Budget Line"
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    budget_start_date = fields.Date(related="budget_id.date_from", readonly=True)
    budget_end_date = fields.Date(related="budget_id.date_to", readonly=True)

    budget_id = fields.Many2one('budget.budget', 'Budget', ondelete='cascade', index=True, required=True)
    state = fields.Selection(related="budget_id.state", readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    planned_amount = fields.Monetary(
        'Budget Amount', required=True,
        default=0.0,
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")
    practical_amount = fields.Monetary(string='Achieved Amount' , default=0.0, store=True)

    over_budget = fields.Monetary(
        string="Over Budget",
        default=0.0,
        compute="_compute_practical_amount",
        help="The amount by which the budget line exceeds its allocated budget.",
        store=True
    )
    count= fields.Integer('Count',computed="_compute_practical_amount",default=0, readonly=True)
    percentage = fields.Float(default=0.0,compute="_compute_achieved_percentage",
        help="Comparison between practical and planned amount. This measure tells you if you are below or over budget.")


    @api.depends("practical_amount", "planned_amount")
    def _compute_achieved_percentage(self):
        for record in self:
            if record.planned_amount:
                record.percentage = (
                    record.practical_amount / record.planned_amount
                ) * 100

    def action_view_analytic_lines(self):
        if not self.budget_id:
            raise UserError("No budget linked to this budget line.")

        budget_start_date = self.budget_id.date_from
        budget_end_date = self.budget_id.date_to

        return {
            "type": "ir.actions.act_window",
            "name": "Analytic Lines",
            "res_model": "account.analytic.line",
            "view_mode": "list",
            "target": "current",
            "context": {
                "default_account_id": self.analytic_account_id.id,
                "budget_start_date": budget_start_date,
                "budget_end_date": budget_end_date,
            },
            "domain": [
                ("account_id", "=", self.analytic_account_id.id),
                ("date", ">=", budget_start_date),
                ("date", "<=", budget_end_date),
                ("amount", "<", 0),
            ],
        }            


   