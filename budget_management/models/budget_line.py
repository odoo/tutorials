from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import SQL

class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget Lines"

    name = fields.Char("Name")
    analytic_account = fields.Many2one("account.analytic.account")
    budget_amount = fields.Integer("Budget Amount", required=True)
    achieved_amount = fields.Float(
        "Achieved Amount", compute="_compute_achieved_amount", store=True
    )
    budget_id = fields.Many2one("budget.budget")
    progress = fields.Float("Achieved (%)", compute="_compute_progress", search="_search_progress")
    account_analytics_line_ids = fields.One2many(
        comodel_name="account.analytic.line", inverse_name="budget_line_id"
    )
    date_from=fields.Date(related='budget_id.date_from')
    date_to=fields.Date(related='budget_id.date_to')
    user_id=fields.Many2one(related='budget_id.user_id')
    
    @api.constrains("achieved_amount", "budget_amount", "account_analytics_line_ids")
    def _check_restriction_on_creation(self):
        for record in self:
            if record.budget_id.over_budget == "restriction":
                if record.achieved_amount > record.budget_amount:
                    raise ValidationError(
                        "Cannot create this analytic line, achieved amount is greater than budget amount"
                    )

    @api.depends("account_analytics_line_ids.amount",)
    def _compute_achieved_amount(self):
        for budget_line in self:
            budget_line.achieved_amount = abs(
                sum(budget_line.account_analytics_line_ids.filtered(lambda l : l.amount<0).mapped("amount"))
            )

    @api.depends("achieved_amount", "budget_amount")
    def _compute_progress(self):
        for record in self:
            if record.budget_amount:
                record.progress = abs(
                    (record.achieved_amount / record.budget_amount) * 100
                )
            else:
                record.progress = 0

    def action_related_account_analytic_lines(self):
        self.ensure_one()
        for record in self:
            action = record.env["ir.actions.act_window"]._for_xml_id(
                "analytic.account_analytic_line_action"
            )
            action["display_name"] = f"Analytic Lines ({record.analytic_account.name})"
            action["domain"] = [("budget_line_id", "=", record.id)]
            action["context"] = {
                "default_budget_line_id": record.id,
                "default_account_id": record.analytic_account.id,
            }
        return action
    
    def _search_progress(self, operator, value):
        sql = SQL("""(
              SELECT bl.id
              FROM budget_line bl
              JOIN account_analytic_line al 
              ON   bl.id = al.budget_line_id
			  JOIN budget_budget bb
			  ON bb.id = bl.budget_id
              WHERE al.amount < 0 AND (al.date >= bb.date_from AND al.date <= bb.date_to)
              GROUP BY bl.id 
              HAVING abs(sum(al.amount))/bl.budget_amount * 100 %s %s
                )""", SQL(operator),value)
        return [('id', 'in', sql)]