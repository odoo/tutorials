from markupsafe import Markup
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class BudgetBudget(models.Model):
    _name = "budget.budget"
    _description = "budget.budget"
    _order = "duration_start_date"
    _inherit = ["mail.thread", "mail.activity.mixin", "avatar.mixin"]

    name = fields.Char()
    description = fields.Char(compute="_compute_description")
    active = fields.Boolean("active", default=True)
    warning = fields.Boolean(compute="_compute_warraning_budget_line")

    duration_start_date = fields.Date(
        "duration_start_date",
    )
    duration_end_date = fields.Date(
        "duration_end_date",
    )
    status = fields.Selection(
        selection=[
            ("Draft", "Draft"),
            ("Confirmed", "Confirmed"),
            ("Revised", "Revised"),
            ("Done", "Done"),
        ],
        default="Draft",
    )
    over_budget = fields.Selection(
        selection=[("warning", "warning"), ("restriction", "restriction")]
    )
    responsible = fields.Many2one(
        "res.users", ondelete="restrict", default=lambda self: self.env.user
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    revise_by = fields.Many2one("res.users", ondelete="restrict", copy=False)
    budget_line_ids = fields.One2many(
        "budget.line", inverse_name="budget_id", string="budget_lines", copy=True
    )

    message_ids = fields.One2many(
        "mail.message",
        "res_id",
        domain=[("model", "=", "budget.budget"), ("model", "=", "budget.line")],
        string="Messages",
    )

    @api.constrains("duration_start_date", "duration_end_date")
    def _constrains_date(self):
        for record in self:
            if record.duration_start_date > record.duration_end_date:
                raise UserError(
                    "Invalid duration! The start date cannot be later than the end date. Please select a valid date range."
                )
            budget = self.env["budget.budget"].search(
                [
                    ("duration_start_date", "=", record.duration_start_date),
                    ("duration_end_date", "=", record.duration_end_date),
                    ("id", "!=", self.id),
                    ("active", "=", True),
                ]
            )
            if budget:
                raise ValidationError(
                    "Warning: A budget already exists for this duration."
                )

    @api.depends("name", "duration_start_date", "duration_end_date")
    def _compute_description(self):
        for record in self:
            if record.name:
                record.description = (
                    record.name
                    + ": "
                    + str(record.duration_start_date)
                    + " to "
                    + str(record.duration_end_date)
                )
            else:
                record.description = ""

    @api.depends("budget_line_ids.budget_achive")
    def _compute_warraning_budget_line(self):
        for record in self:
            record.warning = True
            if record.over_budget == "warning":
                for line in record.budget_line_ids:
                    if line.budget_achive > line.budget_total:
                        record.warning = False

    def action_draft(self):
        for record in self:
            record.status = "Draft"
        return True

    def action_confirm(self):
        for record in self:
            record.status = "Confirmed"
        return True

    def action_done(self):
        for record in self:
            record.status = "Done"
        return True

    def action_revise(self):
        for record in self:
            record.write(
                {"revise_by": self.env.user, "status": "Revised", "active": False}
            )
            revised_budget = record.sudo().copy(
                default={
                    "name": record.name,
                    "status": "Draft",
                    "duration_start_date": record.duration_start_date,
                    "duration_end_date": record.duration_end_date,
                    "active": True,
                }
            )
            record.message_post(
                body=Markup(
                    "%s: <a href='#' data-oe-model='budget.budget' data-oe-id='%s'>%s</a>"
                )
                % (
                    "new budgetid",
                    revised_budget.id,
                    record.name,
                )
            )
        return True

    def action_budget_lines(self):
        return {
            "name": "Budget Lines",
            "view_mode": "list,graph,pivot,gantt",
            "res_model": "budget.line",
            "type": "ir.actions.act_window",
            "context": {
                "default_budget_id": self.id,
            },
            "domain": [("budget_id", "=", self.id)],
        }

    def action_budget_form(self):
        return {
            "name": "Budget",
            "view_mode": "form",
            "res_model": "budget.budget",
            "type": "ir.actions.act_window",
            "res_id": self.id,
        }
