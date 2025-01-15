from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_line_id = fields.Many2one(comodel_name="budget.line", string="Budget Line", ondelete="cascade")
    main_id = fields.Many2one(comodel_name="account.analytic.line.main")

class AccountAnalyticLineMain(models.Model):
    _name = "account.analytic.line.main"

    line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="main_id")
    budget_line_id = fields.Many2one(comodel_name="budget.line", string="Budget Line", ondelete="cascade")
    currency_id = fields.Many2one(comodel_name="res.currency", default=lambda self: self.env.company.currency_id.id)
    budget_amount = fields.Monetary(related="budget_line_id.budget_amount")
    achieved_amount = fields.Monetary(related="budget_line_id.achieved_amount")
    stage = fields.Selection(related="budget_line_id.budget_id.stage")

    @api.model
    def create(self, vals):
        record = super(AccountAnalyticLineMain, self).create(vals)
        record.budget_line_id.main_line_id = record.id
        for line in record.line_ids:
            line.auto_account_id = record.budget_line_id.analytic_account_id
            line.budget_line_id = record.budget_line_id
        return record
