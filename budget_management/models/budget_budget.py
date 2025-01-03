from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from markupsafe import Markup

class BudgetBudget(models.Model):
    _name = "budget.budget"
    _description = "Budget Management"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Budget Name", compute="_compute_name", store=True)
    color = fields.Integer(string="Color", default=0)
    is_favorite = fields.Boolean(default=False)
    stage = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        default="draft",
        required=True,
    )
    responsible_id = fields.Many2one(
        comodel_name="res.users",
        required=True,
        string="Responsible",
        default=lambda self: self.env.user,
    )

    revision_id = fields.Many2one(comodel_name="budget.budget", string="Revision_id", tracking="1")
    parent_revision_id = fields.Many2one(comodel_name="budget.budget", tracking="1")
    on_over_budget = fields.Selection(
        [
            ("warning", "Warning On Budget"),
            ("restrict", "Restriction on Creation"),
        ],
        default="warning",
        required=True,
    )
    period_start = fields.Date(string="Period Start", required=True)
    period_end = fields.Date(string="Period End", required=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    budget_line_ids = fields.One2many(comodel_name="budget.line", inverse_name="budget_id", string="Budget Lines")
    show_warning = fields.Boolean(compute="_compute_show_warning", default=False)

    _sql_constraints = [
        (
            "period_start_end_check",
            "CHECK (period_start < period_end)",
            "The start date must be anterior to the end date.",
        )
    ]

    @api.constrains("period_start", "period_end", "company_id")
    def _check_period_overlap(self):
        for record in self:
            if record.parent_revision_id:
                continue
            record.responsible_id.image_128
            overlapping_budget = self.env["budget.budget"].search(
                [
                    ("id", "!=", record.id),
                    ("company_id", "=", record.company_id.id),
                    ("period_start", "<=", record.period_end),
                    ("period_end", ">=", record.period_start),
                ]
            )
            if overlapping_budget:
                raise ValidationError(
                    f"The budget period overlaps with another budget for the same company: {overlapping_budget.mapped('name')}."
                )

    @api.depends("period_start", "period_end")
    def _compute_name(self):
        for record in self:
            if record.parent_revision_id:
                continue
            if record.period_start and record.period_end:
                start_date = datetime.strftime(record.period_start, "%d-%m-%Y")
                end_date = datetime.strftime(record.period_end, "%d-%m-%Y")
                record.name = f"Budget: {start_date} to {end_date}"
            else:
                record.name = "Budget: No Period Defined"

    @api.depends("budget_line_ids.achieved_amount", "budget_line_ids.budget_amount")
    def _compute_show_warning(self):
        for record in self:
            if self.on_over_budget == "warning":
                record.show_warning = any(
                    line.achieved_amount > line.budget_amount
                    for line in record.budget_line_ids
                )
            else:
                record.show_warning = False

    def action_budget_reset_to_draft(self):
        for record in self:
            if record.stage == "confirmed":
                if record.parent_revision_id:
                    record.parent_revision_id.stage = "confirmed"
                record.stage = "draft"

    def action_budget_to_confirmed(self):
        for record in self:
            if record.stage == "draft":
                if record.parent_revision_id:
                    record.parent_revision_id.stage = "revised"
                    record.parent_revision_id.revision_id = record.id
                record.stage = "confirmed"

    def action_budget_to_revised(self):
        revised_budget = self.copy(
            {
                "name": f"Revised {self.name}",
                "parent_revision_id": self.id,
                "revision_id": False,
                "stage": "draft",
            }
        )

        for budget_line in self.budget_line_ids:
            copied_budget_line = budget_line.copy(
                {
                    "budget_id": revised_budget.id
                }
            )

            for analytic_line in budget_line.analytic_account_id.line_ids.filtered(
                lambda line: line.budget_id == self.id
            ):
                analytic_line.copy(
                    {
                        "budget_id": revised_budget.id,
                        "auto_account_id": copied_budget_line.analytic_account_id.id,
                    }
                )

        return {
            "type": "ir.actions.act_window",
            "name": "Revised Budget Form",
            "res_model": "budget.budget",
            "res_id": revised_budget.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_budget_to_done(self):
        for record in self:
            if record.stage == "confirmed":
                record.stage = "done"
