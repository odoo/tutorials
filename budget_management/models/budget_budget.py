from markupsafe import Markup
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BudgetBudget(models.Model):
    _name = "budget.budget"
    _description = "New Budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    name = fields.Char("Budget Name", compute="_compute_budget_name", required=True)
    active = fields.Boolean(default=True)
    warning_message = fields.Boolean(default=False, compute='_compute_warning')
    date_from = fields.Date("Start Date", required=True)
    date_to = fields.Date("End Date", required=True)
    user_id = fields.Many2one("res.users", "Responsible", default=lambda self: self.env.user)
    revision_id = fields.Many2one("res.users", "Revision_id", default=lambda self: self.env.user)
    company_id = fields.Many2one("res.company", "Company", default=lambda self: self.env.company)
    parent_id = fields.Many2one(string="Revision Of",comodel_name="budget.budget", ondelete="cascade")
    children_ids = fields.One2many(string="Revisions",comodel_name="budget.budget",inverse_name="parent_id")
    budget_line_ids = fields.One2many("budget.line", "budget_id", copy=True)
    over_budget = fields.Selection(
        string="On Over Budget",
        selection=[
            ("warning", "Warning"),
            ("restriction", "Restriction"),
        ],
        required=True,default="warning")
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        required=True,
        default="draft",
    )

    @api.constrains("date_from", "date_to")
    def _constrains_date(self):
        for record in self:
            check_budget = self.env["budget.budget"].search(
                [
                    ("date_from", "=", record.date_from),
                    ("date_to", "=", record.date_to),
                    ("id", "not in", self.ids),
                    ("active", "=", True),
                ]
            )
            if check_budget:
                raise ValidationError(
                    "BUDGET ALREADY EXISTS FOR THIS PERIOD"
                )
            if record.date_from > record.date_to:
                raise ValidationError(
                    "START DATE MUST BE BEFORE END DATE"
                )
           

    @api.depends("date_from", "date_to")
    def _compute_budget_name(self):
        for budget in self:
            if budget.date_from:
                budget.name = _(
                    "Budget :  %(date_from)s to %(date_to)s",
                    date_from=budget.date_from or "",
                    date_to=budget.date_to or "",
                )
            else:
                budget.name = "Budget :  "

    @api.depends("budget_line_ids.achieved_amount","budget_line_ids.budget_amount")
    def _compute_warning(self):
        for record in self:
            if record.over_budget=="warning" and any(line.achieved_amount > line.budget_amount for line in record.budget_line_ids):
                record.warning_message = True
            else:
                record.warning_message=False
                    
    def action_view_budget_lines(self):
        return {
            "name": _("Budget Lines"),
            "type": "ir.actions.act_window",
            "view_mode": "list,graph,pivot,gantt",
            "res_model": "budget.line",
            "target": "self",
            "domain": [("budget_id", "=", self.id)],
        }

    def action_budget_confirm(self):
        self.parent_id.filtered(lambda b: b.state == "confirmed").state = "revised"
        for budget in self:
            budget.state = "revised" if budget.children_ids else "confirmed"

    def action_budget_reset(self):
        self.state = "draft"

    def action_budget_draft(self):
        self.state = "draft"

    def action_budget_done(self):
        self.state = "done"

    def create_revised_budget(self):
        revised = self.browse()
        for budget in self:
            budget.state="revised"
            budget.active=False
            revised_budget = budget.copy(
                default={
                    "name": _("REV %s" % budget.name),
                    "parent_id": budget.id,
                }
            )
            revised += revised_budget
            budget.message_post(
                body=Markup(
                    "%s: <a href='#' data-oe-model='budget.budget' data-oe-id='%s'>%s</a>"
                )
                % (
                    _("New revision"),
                    revised_budget.id,
                    revised_budget.name,
                )
            )
