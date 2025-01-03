from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from markupsafe import Markup


class Budget(models.Model):
    _name = "budget.budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Budget"

    name = fields.Char(string="Budget Name", compute="_compute_name", store=True)
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    user_id = fields.Many2one(
        "res.users", "Responsible", default=lambda self: self.env.user
    )
    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        copy=False,
        readonly=True,
    )
    revision_id = fields.Many2one("budget.budget", string="Revision of", readonly=True)
    on_over_budget = fields.Selection(
        [
            ("warning", "Warning"),
            ("restriction on creation", "Restriction On Creation"),
        ],
        string="On Over Budget",
        default="restriction on creation",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    active = fields.Boolean(default=True)
    color = fields.Integer(string="Color Index")
    budget_line_ids = fields.One2many(
        "budget.lines", "budget_id", string="Budget Lines"
    )
    is_favorite = fields.Boolean(default=False)
    warnings = fields.Boolean(compute="_compute_check_over_budget")

    @api.constrains("date_from", "date_to", )
    def _check_dates(self):
        for record in self:
            if record.date_from >= record.date_to:
                raise ValidationError("Start Date must be before End Date.")
            if record.state in ['draft', 'confirmed']:
                overlapping_budgets = self.env['budget.budget'].search([
                    ('id', '!=', record.id),
                    ('state', 'in', ['draft', 'confirmed']),
                    ('date_from', '<=', record.date_to),
                    ('date_to', '>=', record.date_from),
                ])
                if overlapping_budgets:
                    raise UserError("Cannot create or update this budget because it overlaps with another budget.")

    @api.depends("date_from", "date_to")
    def _compute_name(self):
        for record in self:
            record.name = f"Bugdet{record.date_from} - {record.date_to}"

    @api.depends("budget_line_ids")
    def _compute_check_over_budget(self):
        for record in self:
            if record.on_over_budget == "warning" and any(
                ob.practical_amount > ob.planned_amount for ob in record.budget_line_ids
            ):
                record.warnings = True
            else:
                record.warnings = False

    def action_budget_confirmed(self):
        if self.state != "draft":
            raise ValidationError("Only budgets in draft state can be confirmed.")
        self.write({"state": "confirmed"})

    def action_budget_revise(self):
        if self.state != "confirmed":
            raise UserError("Only confirmed budgets can be revised.")
        self.ensure_one()
        new_budget_vals = self.copy_data()[0]
        new_budget_vals["revision_id"] = self.id
        new_budget_vals["state"] = "draft"
        # self.active = False
        self.state = "revised"
        new_budget = self.create(new_budget_vals)

        for line in self.budget_line_ids:
            line.copy({"budget_id": new_budget.id})

        message = f"Budget has been revised. A new budget record has been created: <a href='#id={new_budget.id}&model=budget.budget' target='__blank'>{new_budget.name}</a>"
        self.message_post(body=Markup(message))
        return new_budget

    def action_budget_draft(self):
        if self.state not in ["confirmed", "revised"]:
            raise ValidationError(
                "Only confirmed or revised budgets can be set back to draft."
            )
        self.write({"state": "draft"})

    def action_budget_done(self):
        if self.state != "revised":
            raise ValidationError("Only revised budgets can be marked as done.")
        self.write({"state": "done"})

    def action_budget_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Budget Wizard",
            "res_model": "budget.wizard",
            "view_mode": "form",
            "target": "new",
        }
