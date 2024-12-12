from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from markupsafe import escape, Markup


class Budget(models.Model):
    _name = "budget.budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = " "

    name = fields.Char(compute="_compute_budget_name", store=True, readonly=True)
    active = fields.Boolean(default=True)
    is_favorite = fields.Boolean(default=False)
    color = fields.Integer(string="Color Index")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        required=True,
        default="draft",
        tracking=True,
    )
    on_over_budget = fields.Selection(
        selection=[("warning", "Warning"), ("restriction", "Restriction")],
        tracking=True,
    )
    responsible = fields.Many2one(
        comodel_name="res.users",  # Assuming you want a link to Odoo users
        string="Responsible",
        tracking=True,
    )
    revision_id = fields.Many2one(
        comodel_name="res.users",  # Assuming you want a link to Odoo users
        tracking=True,
        readonly=True,
        string="Revised by"
    )
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="Expiration Date", required=True, index=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    budget_line_ids = fields.One2many(
        comodel_name="budget.management.budget.lines", inverse_name="budget_id"
    )
    warnings = fields.Text(compute="_check_over_budget")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    @api.depends("date_start", "date_end")
    def _compute_budget_name(self):
        for record in self:
            if record.date_start and record.date_end:
                start_date = record.date_start
                end_date = record.date_end
                if (
                    start_date.year == end_date.year
                    and start_date.month == end_date.month
                ):
                    record.name = f"Budget - {start_date.strftime('%B %Y')}"
                else:
                    record.name = f"Budget - {start_date.strftime('%d %B, %Y')} to {end_date.strftime('%d %B, %Y')}"
            else:
                record.name = "Unknown Budget"

    def onclick_reset_to_draft(self):
        for record in self:
            if record.state != "draft":
                record.state = "draft"

    def onclick_confirmed(self):
        for record in self:
            if record.state == "draft":
                record.state = "confirmed"

    def onclick_revise(self):
        for record in self:
            if record.state != "confirmed":
                raise UserError("Only confirmed budgets can be revised.")

            if record.state == "confirmed":
                record.revision_id = self.env.user
                record.state = "revised"
                record.active = False

                new_budget = record.copy(
                    {"revision_id": None, "state": "draft", "active": True}
                )

                for budget_line in record.budget_line_ids:
                    self.env["budget.management.budget.lines"].create(
                        {
                            "budget_id": new_budget.id,
                            "name": budget_line.name,
                            "budget_amount": budget_line.budget_amount,
                            "achieved_amount": budget_line.achieved_amount,
                            "achieved_percentage": budget_line.achieved_percentage,
                            "analytic_account_id": budget_line.analytic_account_id.id,
                            "currency_id": budget_line.currency_id.id,
                        }
                    )

                action = self.env.ref(
                    "budget_management.action_budget_management_menu_budget"
                )
                record.message_post(
                    body=Markup(
                        f'<a href="odoo/action-{action.id}/{new_budget.id}">{new_budget.name}</a>.'
                    )
                )

    def onclick_done(self):
        for record in self:
            if record.state in ["confirmed", "revised"]:
                record.state = "done"

    @api.constrains("date_start", "date_end")
    def _check_period_overlap(self):
        for record in self:
            overlapping_budgets = self.search(
                [
                    ("id", "!=", record.id),
                    ("date_start", "<=", record.date_start),
                    ("date_end", ">=", record.date_end),
                    ("company_id", "=", record.company_id.id),
                ]
            )
            overlapping_non_revised = False

            for budget in overlapping_budgets:
                if budget.state != "revised":
                    overlapping_non_revised = True
                    break

            if overlapping_non_revised:
                raise ValidationError(
                    "Cannot create overlapping budgets for the same period and company. If not displayed your selected period budget! please check archived budgets"
                )

    @api.depends("budget_line_ids.over_budget")
    def _check_over_budget(self):
        for record in self:
            if (
                record.on_over_budget == "warning"
                and any(ob > 0 for ob in record.budget_line_ids.mapped("over_budget")) > 0
            ):
                record.warnings = "Achieved amount exceeds the budget!"
            else:
                record.warnings = False
