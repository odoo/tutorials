from odoo import fields, models, exceptions, api
from markupsafe import Markup

class BudgetCreate(models.Model):
    _name = 'budget.budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Budget"
    
    name = fields.Char(required=True)
    user_id = fields.Many2one("res.users")
    period_start_date = fields.Date(required=True)
    period_end_date = fields.Date(index=True)
    con_color = fields.Integer()
    over_budget = fields.Selection(
        [
            ('warning', 'Warning'),
            ('restriction', 'Restriction')
        ],
        default="warning"
    ) 
    budget_line_ids = fields.One2many('budget.line', 'budget_id')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('conformed', 'Conformed'),
            ('revised', 'Revised'),
            ('done', 'Done')
        ],
        default='draft'
    )
    company_id = fields.Many2one('res.company')
    active = fields.Boolean(default=True)
    message_ids = fields.One2many(
        'mail.message', 'res_id', 
        domain=[('model', '=', 'budget.budget'), ('model', '=', 'budget.line')],
        string="Messages"
    )
    is_warning = fields.Boolean(default=False, compute="_compute_warning_message")

    @api.constrains('period_start_date', 'period_end_date')
    def check_unique_duration(self):
        for record in self:
            check_duration = self.env['budget.budget'].search(
                [
                    ('period_start_date', '=', record.period_start_date),
                    ('period_end_date', '=', record.period_end_date),
                    ('active', '=', True),
                    ('id', 'not in', self.ids)
                ]
            )
            if check_duration:
                raise exceptions.ValidationError(f"please check the duration, already Present {record.period_start_date} to {record.period_end_date}")

    @api.depends('budget_line_ids.archived_amount', 'budget_line_ids.budget_amount', 'is_warning')
    def _compute_warning_message(self):             # Compute Method : Manage the warning message 
        for record in self:
            is_warning = False
            for line in record.budget_line_ids:
                if line.archived_amount and line.budget_amount and line.archived_amount > line.budget_amount and record.over_budget == 'warning':
                    is_warning = True
                    break  
            record.is_warning = is_warning

    def action_budget_line_form(self):          # Action Button : for open Budget Lines
        action = (
            self.env["ir.actions.act_window"]
            .with_context({"active_id": self.id})
            ._for_xml_id("budget_management.act_budget_lines_view")
        )
        action["display_name"] = self.name
        return action

    def action_budget_form_view(self):              # Action Button : for open budget Form
        return {
            "type": "ir.actions.act_window",
            "res_model": "budget.budget",
            "view_mode": "form",
            "res_id": self.id
        }       
    
    def action_to_draft(self):              # Button Method : for draft
        self.state = 'draft'
    
    def action_to_conform(self):            # Button Method : for conformed
        self.state = 'conformed'

    def action_to_revised(self):            # Button Method : for revised
        for record in self:
            if record.state == 'conformed':
                record.state = 'revised'
                record.active = False

                orignal_record = record.browse(record.id)

                new_record = orignal_record.copy(default={
                    'state': 'draft',
                    'period_start_date': record.period_start_date,  
                    'period_end_date': record.period_end_date,  
                    'name': f"Revised: {record.name}",  
                    'active': True
                })

                for line in record.budget_line_ids:
                    line.copy({
                        'budget_id': new_record.id,
                    })

                message_body = f"Revised to: <a href='/web#id={new_record.id}&model=budget.budget' target='_blank'>{new_record.name}</a>"
                record.message_post(body=Markup(message_body))

            else:
                raise exceptions.ValidationError("The budget is not conformed yet...")

    def action_to_done(self):       # Button Method : for done
        self.state = 'done'
