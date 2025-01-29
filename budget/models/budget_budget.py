from odoo import models, api, fields
from odoo.exceptions import ValidationError, UserError
from markupsafe import Markup
from odoo.tools import SQL

class BudgetBudget(models.Model):
    _name = "budget.budget"
    _inherit = ["mail.thread"]

    budget_line_ids = fields.One2many(
        comodel_name="budget.budget.line", inverse_name="budget_id"
    )
    account_analytic_line_ids = fields.One2many(
        comodel_name="account.analytic.line", inverse_name="budget_id"
    )

    color = fields.Integer(string="Color")
    is_favorite = fields.Boolean(string="Favorite", default=False)
    name = fields.Char(string="Budget Name", compute="_compute_budget_name")
    date_start = fields.Date(string="From", required=True)
    date_end = fields.Date(string="to", required=True)
    active = fields.Boolean(
        string="Active", default=True, readonly=True
    )  # not archived by default
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    responsible_id = fields.Many2one(
        string="Responsible", comodel_name="res.users", required=True
    )
    revision_id = fields.Many2one(
        string="Revision_id", comodel_name="res.users", readonly=True
    )  # revised budget it
    parent_budget_id = fields.Many2one(
        string="Parent Budget", comodel_name="budget.budget", readonly=True
    )
    warning_message = fields.Char(
        string="warning", compute="_compute_warning_message", default="None", store=True
    )
    # on revision archive the current budget and make a new budget with same specs

    state = fields.Selection(
        string="State",
        default="draft",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
    )
    on_over_budget_type = fields.Selection(
        string="On Over Budget",
        default="warning_on_budget",
        selection=[
            ("warning_on_budget", "Warning on Budget"),
            ("restriction_on_creation", "Restriction on Creation"),
        ],
    )
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for record in self:
            if(record.state not in ('draft', 'done')):
                raise UserError("Deletion is only allowed in the Draft and done stages.")

    @api.depends("budget_line_ids.achieved_amount", "budget_line_ids.budget_amount")
    def _compute_warning_message(self):
        for record in self:
            if record.on_over_budget_type == "warning_on_budget":
                flag=False
                for line in record.budget_line_ids:
                    if (line.achieved_amount > line.budget_amount):
                        flag = True
                        record.warning_message = f"budget with account {line.analytic_account_id.name} is exceeding the limit which is ${line.budget_amount}"
                        break
                if(not flag):
                    record.warning_message= "None"
            else:
                record.warning_message = "None"

    @api.constrains("date_start", "date_end")
    def _check_period_to_be_unique(self):
        for record in self:
            existing_budget = self.search(
                domain=[
                    ("id", "!=", record.id),
                    ("date_start", "=", record.date_start.strftime('%Y-%m-%d')),
                    ("date_end", "=", record.date_end.strftime('%Y-%m-%d')),
                    ("active", "!=", False),  # skip the archived budgets
                ]
            )
            if len(existing_budget) > 0:
                raise ValidationError("A budget with the same date range already exists")

    @api.depends("date_start", "date_end")
    def _compute_budget_name(self):
        for record in self:
            if record.date_start and record.date_end:
                record.name = f"Budget: {record.date_start.strftime('%m/%d/%Y')} to {record.date_end.strftime('%m/%d/%Y')}"
            else:
                record.name = "Budget: New"

    def action_budget_confirm(self):
        for record in self:
            if record.state == "draft":
                record.state = "confirmed"

    def action_budget_revise(self):
        for record in self:
            if record.state == "confirmed":
                record.active = False
                revised_budget = record.copy(
                    {
                        "name": record.name,
                        "parent_budget_id": record.id,
                        "active": True
                    }
                )

                record.sudo().message_post(
                    body=Markup(
                        f'New revise budget Link: <a href="#" data-oe-model="budget.budget" data-oe-id="{revised_budget.id}">{revised_budget.name}</a>'
                    ),
                )

                record.revision_id = self.env.user.id
                # create new budget with same specs and mark this archived
                record.state = "revised"

    def action_budget_done(self):
        for record in self:
            if record.state not in ("draft", "revised"):
                record.state = "done"

    def action_open_budget(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Budget",
            "res_model": "budget.budget",
            "view_type": "form",
            "view_mode": "form",
            "target": "current",
            "res_id": self.id,
        }

    def action_open_budget_lines(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Budget Lines",
            "res_model": "budget.budget.line",
            "view_mode": "list,graph,pivot,gantt",
            "domain": [("budget_id", "=", self.id)],
        }


    # @api.model_create_multi
    # def create(self, vals):
    #     for val in vals:
    #         existing_budget= self.env['budget.budget'].search([
    #                 ("date_start", "=", val['date_start'].strftime('%Y-%m-%d')),
    #                 ("date_end", "=", val['date_end'].strftime('%Y-%m-%d')),
    #                 ("active", "!=", False),  # skip the archived budgets
    #             ]
    #         )

    #         if existing_budget:
    #             raise ValidationError("same range budget exists")
        
    #     super().create(vals)