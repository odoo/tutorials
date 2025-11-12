from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class Budget(models.Model):
    _name = "budget.budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Budget Management"

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
        comodel_name="res.users",
        string="Responsible",
        tracking=True,
    )
    revision_id = fields.Many2one(
        comodel_name="budget.budget",  # This should point to the same budget model
        tracking=True,
        readonly=True,
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
    warnings = fields.Text(readonly=True)
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
                start_date = record.date_start.strftime("%Y-%m")
                end_date = record.date_end.strftime("%Y-%m")
                record.name = f"Budget {start_date} to {end_date}"
            else:
                record.name = "Unknown Budget"

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
            if overlapping_budgets:
                raise ValidationError(
                    "Cannot create overlapping budgets for the same period and company."
                )

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

            # Archive the current record and set its state to 'revised'
            record.sudo().write({
                'state': 'revised',
                'active': False,  # Archive the original record
                'revision_id': record.id,  # Set the revision_id to refer to the original budget
            })

            # Create a duplicate budget (this will be the revised budget)
            duplicate = record.copy()

            # Manually copy related budget lines to the new budget (duplicate)
            for line in record.budget_line_ids:
                self.env["budget.management.budget.lines"].create({
                    'name': line.name,
                    'budget_id': duplicate.id,  # Link to the duplicated budget
                    'budget_amount': line.budget_amount,
                    'analytic_account_id': line.analytic_account_id.id,
                    # Add any other necessary fields here
                })

            # Update the duplicate record's state and fields
            duplicate.sudo().write({
                'state': 'draft',  # Set the duplicate budget's state to draft
                'active': True,  # Set the new record as active
                'responsible': self.env.user.id,  # Set the current user as responsible for the revised budget
                'revision_id': record.id,  # Set the revision_id to point to the original budget (parent budget)
                'name': f"{record.name} (Revised)",  # Adjust the name for clarity
            })

            # Log a message for traceability
            record.message_post(
                body="The budget has been revised. A new draft budget has been created.",
                message_type="notification",
            )


    def onclick_done(self):
        for record in self:
            if record.state in ["confirmed", "revised"]:
                record.state = "done"
