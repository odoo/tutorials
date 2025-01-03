from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget Line"

    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", required=True)
    name = fields.Char(related='analytic_account_id.name')
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    budget_amount = fields.Monetary(required=True)
    achieved_amount = fields.Monetary(compute="_compute_achieved_amount", store=True)
    achieved_percentage = fields.Float(compute="_compute_achieved_percentage")
    budget_id = fields.Many2one(comodel_name="budget.budget", string="Budget", ondelete="cascade")
    date_start = fields.Date(related="budget_id.period_start")
    date_stop = fields.Date(related="budget_id.period_end")
    responsible_id = fields.Many2one(related='budget_id.responsible_id', store=True)
    line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="budget_line_id")
    main_line_id = fields.Many2one(comodel_name="account.analytic.line.main")

    @api.constrains("budget_amount", "achieved_amount")
    def _check_achieved_amount(self):
        for record in self:
            if record.achieved_amount > record.budget_amount and self.budget_id.on_over_budget == "restrict":
                raise ValidationError("Achieved amount cannot be greater than budget amount")

    @api.depends("budget_amount", "achieved_amount")
    def _compute_achieved_percentage(self):
        for record in self:
            if record.budget_amount:
                record.achieved_percentage = (record.achieved_amount / record.budget_amount) * 100
            else:
                record.achieved_percentage = 0

    @api.depends("main_line_id.line_ids.amount")
    def _compute_achieved_amount(self):
        for record in self:
            record.achieved_amount = 0
            if self.main_line_id:
                record.achieved_amount = sum(
                record.main_line_id.line_ids.mapped("amount")
            )

    def action_open_account_analytic_line_list(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Analytic Lines",
            "res_model": "account.analytic.line.main",
            "res_id": self.main_line_id.id,
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_budget_line_id": self.id,
                "default_auto_account_id": self.analytic_account_id.id,
            },
        }
