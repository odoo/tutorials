from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class BudgetBudget(models.Model):
    _name = "budget.budget"
    _description = "Budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
        ],
        string="State",
        default="draft",
        required=True,
        index=True,
    )
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    user_id = fields.Many2one(
        "res.users", string="Responsible", default=lambda self: self.env.user
    )
    budget_line_ids = fields.One2many("budget.line", "budget_id", string="Budget Lines")
    revision_id = fields.Many2one(
        "budget.budget", string="Revision_id", readonly=True, tracking=True
    )
    parent_id = fields.Many2one(
        "budget.budget", string="Parent_id", ondelete="cascade", readonly=True
    )
    on_over_budget = fields.Selection(
        selection=[
            ("warning", "Warning on Budget"),
            ("restrict", "Restriction on Creation"),
        ],
        default="warning",
    )
    over_budget = fields.Boolean(compute="_compute_over_budget")
    color = fields.Integer(default=0)
    is_favorite = fields.Boolean(default=False)

    @api.constrains("date_from", "date_to")
    def _check_unique_period(self):
        for record in self:
            budget = self.search(
                [
                    ("date_from", ">=", record.date_from),
                    ("date_from", "<=", record.date_to),
                    ("parent_id", "=", record.parent_id.id),
                ],
                limit=1,
            )
            if budget and budget.id != record.id:
                raise UserError("A budget with the same period already exists.")

    @api.ondelete(at_uninstall=False)
    def _change_state_on_unlink(self):
        for record in self:
            if record.parent_id:
                record.parent_id.write({"state": "confirmed"})

    @api.depends("date_from", "date_to")
    def _compute_name(self):
        for record in self:
            if not record.name:
                if record.date_from and record.date_to:
                    record.name = f"Budget: {record.date_from} to {record.date_to}"

    @api.depends("budget_line_ids.achieved_amount", "budget_line_ids.budget_amount")
    def _compute_over_budget(self):
        for record in self:
            record.over_budget = any(
                line.is_above_budget for line in record.budget_line_ids
            )

    def action_confirm(self):
        if self.parent_id:
            self.parent_id.write({"state": "revised"})
        self.write({"state": "confirmed"})

    def action_revised(self):
        new_record = self.env["budget.budget"].create(
            {
                "name": f"Revised {self.name}",
                "date_from": self.date_from,
                "date_to": self.date_to,
                "state": "draft",
                "parent_id": self.id,
                "budget_line_ids": [
                    Command.create(
                        {
                            "budget_analytic_id": line.budget_analytic_id.id,
                            "budget_amount": line.budget_amount,
                            "achieved_amount": line.achieved_amount,
                        }
                    )
                    for line in self.budget_line_ids
                ],
            }
        )
        self.write({"revision_id": new_record.id})
        return {
            "type": "ir.actions.act_window",
            "name": "Revised Budget",
            "res_model": "budget.budget",
            "view_mode": "form",
            "res_id": new_record.id,
            "target": "current",
        }

    def action_done(self):
        self.write({"state": "done"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})
