from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    budget_id = fields.Many2one('budget.budget', "Associated Budget")
    budget_line = fields.Many2one('budget.line', "Budget Line")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)

        for record in res:
            if record.budget_id.on_over_budget == 'restrict' and abs(record.amount) + record.budget_line.achieved_amount > record.budget_line.budget_amount:
                raise UserError("The amount value is exceeding the budget amount")
            
            record.budget_line._compute_achieved_amount()
            record.budget_line._compute_over_budget()
        return res

    def write(self, vals):
        for record in self:
            if record.budget_id.on_over_budget == 'restrict' and abs(record.amount) + record.budget_line.achieved_amount > record.budget_line.budget_amount:
                raise UserError("The amount value is exceeding the budget amount")
            
            record.budget_line._compute_achieved_amount()
            record.budget_line._compute_over_budget()
        super().write(vals)
