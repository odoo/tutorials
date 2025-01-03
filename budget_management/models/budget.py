# Part of Odoo. See LICENSE file for full copyright and licensing details.

from markupsafe import Markup

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Budget(models.Model):
    _name = "budget"
    _description = "Budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        "Budget Name", compute="_compute_name", store=True, readonly=True
    )
    parent_id = fields.Many2one(
        string="Revision Of",
        comodel_name="budget",
        ondelete="cascade",
        readonly=True
    )
    children_ids = fields.One2many(
        string="Revisions",
        comodel_name="budget",
        inverse_name="parent_id",
    )
    user_id = fields.Many2one(
        "res.users", "Responsible", default=lambda self: self.env.user
    )
    date_from = fields.Date("Start Date", required=True)
    date_to = fields.Date("End Date", required=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Open"),
            ("revised", "Revised"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        required=True,
        default="draft",
        readonly=True,
        copy=False,
        tracking=True,
    )
    on_over_budget = fields.Selection(
        string="On Over Budget",
        selection=[
            ("warning", "Warning on Budget"),
            ("restriction", "Restriction on Creation"),
        ],
        required=True,
        default="warning",
        copy=False,
    )
    budget_line_ids = fields.One2many(
        "budget.line", "budget_id", "Budget Lines", copy=True
    )
    color = fields.Integer(
        "Color",
        default=7,
        compute="_compute_color",
    )
    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    is_favorite = fields.Boolean("Favorite")
    @api.constrains("parent_id")
    def _check_parent_id(self):
        for budget in self:
            if budget._has_cycle():
                raise ValidationError(
                    _("You cannot create recursive revision of budget.")
                )

    @api.constrains("date_from", "date_to")
    def _check_unique_dates(self):
        for record in self:
            existing_budget = self.search(
                [
                    ("id", "!=", record.id),
                    ("date_from", "=", record.date_from),
                    ("date_to", "=", record.date_to),
                ]
            )
            if existing_budget and not record.parent_id:
                raise ValidationError(
                    "A budget with the same date range already exists."
                )

    @api.depends("budget_line_ids")
    def _compute_color(self):
        for record in self:
            isOver = any(line.is_above_budget for line in record.budget_line_ids)
            if isOver and record.on_over_budget == "warning":
                record.color = 3
            elif isOver and record.on_over_budget == "restriction":
                record.color = 1
            else:
                record.color = 7

    @api.depends("date_from", "date_to")
    def _compute_name(self):
        for record in self:
            if record.date_from and record.date_to:
                record.name = f"Budget: {record.date_from.strftime('%m/%d/%Y')} to {record.date_to.strftime('%m/%d/%Y')}"
            else:
                record.name = "Budget: Period"

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        if any(budget.state not in ("draft", "canceled") for budget in self):
            raise UserError(
                _("Deletion is only allowed in the Draft and Canceled stages.")
            )

    def action_budget_confirm(self):
        self.parent_id.filtered(lambda b: b.state == "confirmed").state = "revised"
        for budget in self:
            budget.state = "revised" if budget.children_ids else "confirmed"

    def action_budget_draft(self):
        self.state = "draft"

    def action_budget_cancel(self):
        self.state = "canceled"

    def action_budget_done(self):
        self.state = "done"

    def create_revised_budget(self):
        for budget in self:
            revised_budget = budget.copy(
                default={
                    "name": budget.name,
                    "parent_id": budget.id,
                }
            )
            budget.message_post(
                body=Markup(
                    "%s: <a href='#' data-oe-model='budget' data-oe-id='%s'>%s</a>"
                )
                % (
                    _("New revision"),
                    revised_budget.id,
                    revised_budget.name,
                )
            )
        return revised_budget._get_records_action()

    def action_open_budget_lines(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Budget Lines"),
            "res_model": "budget.line",
            "view_mode": "list,pivot,graph,gantt",
            "domain": [("budget_id", "in", self.ids)],
        }
