from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetBudget(models.Model):
    _name = "budget.budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Budget"

    name = fields.Char(string="Budget Name", compute="_compute_budget_name", store=True)
    responsible = fields.Many2one("res.users", string="Responsible")
    revision_id = fields.Many2one("budget.budget", string="Revision", tracking=True)
    period_start_date = fields.Date(string="Period")
    period_end_date = fields.Date(string="->")
    company = fields.Many2one("res.company", string="Company")
    on_over_budget = fields.Selection(
        string="On Over Budget",
        selection=[
            ("warning", "Warning on Budget"),
            ("restriction", "Restriction on Budget"),
        ],
    )
    over_budget_visible = fields.Boolean(
        string="Over Budget Visible",
        compute="_compute_over_budget_visible",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        default="draft",
    )
    budget_line_ids = fields.One2many("budget.line", "budget_id", string="Budget Lines")
    color = fields.Integer(string="Color")
    warning_message = fields.Char(
        string="Warning Message", default="", compute="_compute_warning_message"
    )
    parent_id = fields.Many2one("budget.budget", string="Parent Budget")

    @api.constrains("period_start_date", "period_end_date")
    def _check_period(self):
        for record in self:
            if record.id:
                budgets = self.search(
                    [
                        ("id", "!=", record.id),
                        ("period_start_date", "<", record.period_end_date),
                        ("period_end_date", ">", record.period_start_date),
                        ("parent_id", "=", record.parent_id.id),
                    ]
                )
                if budgets:
                    raise ValidationError(
                        "Not allowed to create budget with same period"
                    )

    @api.depends("period_start_date", "period_end_date")
    def _compute_budget_name(self):
        for record in self:
            if record.parent_id:
                record.name = f"Revised : {record.parent_id.name}"
            elif record.period_start_date and record.period_end_date:
                record.name = (
                    f"Budget : {record.period_start_date} to {record.period_end_date}"
                )
            else:
                record.name = "Budget"

    @api.depends("budget_line_ids.achieved_amount", "budget_line_ids.budget_amount")
    def _compute_over_budget_visible(self):
        for record in self:
            record.over_budget_visible = True
            for line in record.budget_line_ids:
                if (
                    line.achieved_amount
                    and line.budget_amount
                    and line.achieved_amount > line.budget_amount
                ):
                    record.over_budget_visible = False
                    break

    @api.depends("on_over_budget")
    def _compute_warning_message(self):
        for record in self:
            if record.on_over_budget == "warning":
                record.warning_message = "Warning on Budget"
            else:
                record.warning_message = ""

    def action_reset_to_draft(self):
        for record in self:
            if record.state in ["confirmed", "revised"]:
                record.state = "draft"
        return True

    def action_confirm(self):
        for record in self:
            if record.state == "draft":
                record.state = "confirmed"
                if record.parent_id: 
                    record.parent_id.state = "revised"
                    record.parent_id.revision_id.name = record.name
        return True

    def action_revise(self):
        for record in self:
            if record.state == "confirmed":
                new_budget = record.copy(
                    default={
                        "state": "draft",
                        "parent_id": record.id,
                        "period_start_date": record.period_start_date,
                        "period_end_date": record.period_end_date,
                    }
                )
                self.revision_id = new_budget
                return {
                    "name": "Revised Budget",
                    "type": "ir.actions.act_window",
                    "res_model": "budget.budget",
                    "res_id": new_budget.id,
                    "view_mode": "form",
                    "target": "current",
                }

    def action_set_to_done(self):
        for record in self:
            if record.state in ["confirmed", "revised"]:
                record.state = "done"
        return True

    def open_budget_form_view(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "budget.budget",
            "view_mode": "form",
            "target": "main",
            "res_id": self.id,
        }

    def action_create_multiple_budget(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "multiple.budget.wizard",
            "view_mode": "form",
            "name": "Create Multiple Budget",
            "target": "new",
        }
