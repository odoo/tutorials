from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BudgetBudget(models.Model):
    _name = "budget.budget"
    _description = "Budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(compute="_compute_name")
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(default=True)
    show_warning = fields.Boolean(default=False, compute="_compute_show_warning")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        default="draft",
    )
    action_over_budget = fields.Selection(
        [("warning", "Warning"), ("restrict", "Restrict")],
        default="warning",
    )
    user_id = fields.Many2one("res.users", string="Responsible")
    company_id = fields.Many2one("res.company", string="Company")
    parent_id = fields.Many2one(
        string="Revision Of",
        comodel_name="budget.budget",
        ondelete="cascade",
    )
    budget_line_ids = fields.One2many(
        "budget.budget.line", "budget_id", string="Budget lines"
    )
    children_ids = fields.One2many(
        string="Revisions",
        comodel_name="budget.budget",
        inverse_name="parent_id",
    )

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for budget in self:
            if (
                budget.date_from
                and budget.date_to
                and budget.date_from > budget.date_to
            ):
                raise ValidationError("The start date must be before the end date.")

    # period must be unique for all active budget
    @api.constrains("date_from", "date_to")
    def _check_date(self):
        for budget in self:
            if budget.date_from and budget.date_to:
                existing_budgets = self.search(
                    [
                        ("date_from", "=", budget.date_to),
                        ("date_to", "=", budget.date_from),
                        ("active", "=", True),
                        ("id", "!=", budget.id),
                    ]
                )
                if existing_budgets:
                    raise ValidationError(
                        "Budget period must be unique for all active budgets."
                    )

    @api.depends("budget_line_ids.achieved_amount")
    def _compute_show_warning(self):
        for record in self:
            if record.action_over_budget == "warning" and any(
                ob.achieved_amount > ob.amount for ob in record.budget_line_ids
            ):
                record.show_warning = True
            else:
                record.show_warning = False

    @api.depends("name", "date_from", "date_to")
    def _compute_name(self):
        for budget in self:
            if budget.date_from and budget.date_to:
                budget.name = "Budget: %s - %s " % (
                    budget.date_from.__format__("%d/%m/%Y"),
                    budget.date_to.__format__("%d/%m/%Y"),
                )
            else:
                budget.name = "Budget: (from) - (to)"

    def action_budget_confirm(self):
        self.parent_id.filtered(lambda b: b.state == "confirmed").state = "revised"
        for budget in self:
            budget.state = "revised" if budget.children_ids else "confirmed"

    def action_budget_draft(self):
        self.state = "draft"

    def action_budget_done(self):
        self.state = "done"

    def create_revised_budget(self):
        revised = self.browse()
        for budget in self:
            budget.state = "revised"
            budget.active = False
            revised_budget = budget.copy(
                default={
                    "name": budget.name,
                    "parent_id": budget.id,
                    "active": True,
                }
            )

            revised += revised_budget
            budget.message_post(
                body=Markup(
                    "%s: <a href='#' data-oe-model='budget.budget' data-oe-id='%s'>%s</a>"
                )
                % (
                    "New revision",
                    revised_budget.id,
                    revised_budget.name,
                )
            )
        return revised._get_records_action()

    def action_open_budget_lines(self):
        return {
            "name": "Budget Lines",
            "view_mode": "list,graph,pivot,gantt",
            "res_model": "budget.budget.line",
            "type": "ir.actions.act_window",
            "domain": [("budget_id", "=", self.id)],
        }
