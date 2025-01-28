from odoo import models, fields, api
from markupsafe import Markup
from odoo.exceptions import ValidationError

class BudgetBudget(models.Model):
    _name = 'budget.budget'
    _description = 'Budget'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    message_ids = fields.One2many(
        'mail.message', 'res_id', 
        domain=[('model', '=', 'budget.budget'), ('model', '=', 'budget.line')],
        string="Messages"
    )

    name = fields.Char("Name", compute='_compute_name', store='True')
    starting_date = fields.Date("Starting Date", required=True)
    ending_date = fields.Date("Ending Date", required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('revised', 'Revised'),
        ('done', 'Done'),
    ],
        default='draft',
        # tracking=True
    )

    responsible_person = fields.Many2one("res.users", string="Responsible Person")
    revision_id = fields.Many2one("res.users", string="Revision ID", readonly=True)

    revised_from = fields.Boolean("Revised From")
    revised_to = fields.Boolean("Revised To")

    active = fields.Boolean("is Active", default=True)

    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    on_over_budget = fields.Selection([
        ('warning', "Warning on Budget"),
        ('restrict', "Restriction on Creation"),
    ], required=True, default='warning')

    warning_message = fields.Boolean("Warning Message", compute="_compute_warning")
    budget_line_ids = fields.One2many('budget.line', 'budget_id', "Budget Lines")

    @api.depends('budget_line_ids.achieved_amount', 'budget_line_ids.budget_amount')
    def _compute_warning(self):
        for record in self:
            for budget_line in record.budget_line_ids:
                if budget_line.achieved_amount > budget_line.budget_amount:
                    record.warning_message = True
                    break
                else:
                    record.warning_message = False
            if record.warning_message:
                break

    @api.constrains('starting_date', 'ending_date')
    def _check_if_duration_is_free(self):
        for record in self:
            budget_exists = self.env['budget.budget'].search([
                ("starting_date", "=", record.starting_date),
                ("ending_date", "=", record.ending_date),
                ("id", "!=", record.id),
                ("active", "=", True)
            ])

            if budget_exists:
                raise ValidationError("Budget with this duration already exists.")

    def action_view_budget_lines(self):
        action = (
            self.env["ir.actions.act_window"]
            .with_context({"active_id": self.id})
            ._for_xml_id("budget_management.budget_line_action")
        )
        action["display_name"] = self.name
        return action

    def action_view_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'budget.budget',
            'view_mode': 'form',
            'res_id': self.id,
        }

    @api.depends('starting_date', 'ending_date')
    def _compute_name(self):
        for record in self:
            record.name = f'Budget: {record.starting_date} to {record.ending_date}' if record.starting_date and record.ending_date else 'New Budget'

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_revise(self):
        for record in self:
            breakpoint()
            record.state = 'revised'
            record.active = False

            record.revision_id = self.env.user.id

            revised_record = record.copy({
                'state': 'draft',
                'active': True
            })

            for line in record.budget_line_ids:
                line.copy({
                    'budget_id': revised_record.id,
                })

            last_name = record.name

            revised_record.starting_date = record.starting_date
            revised_record.ending_date = record.ending_date

            revised_record._compute_name()
            revised_record.name = f'REV {last_name}'

            revised_record.revised_from = record.id
            record.revised_to = revised_record.id

            action_id = self.env.ref('budget_management.budget_action').id

            message_body = f"Revised to: <a href='/odoo/action-{action_id}/{revised_record.id}'>{revised_record.name}</a>"
            record.message_post(body=Markup(message_body))

            message_body = f"Revised from: <a href='/odoo/action-{action_id}/{record.id}'>{record.name}</a>"
            revised_record.message_post(body=Markup(message_body))

    def action_done(self):
        for record in self:
            record.state = 'done'
