from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _inherit = ['mail.thread']
    _description = 'Visits scheduled for the property'
    _rec_name = 'property_title'

    finished = fields.Boolean(default=True)
    reminder = fields.Boolean(default=False)
    property_id = fields.Many2one(comodel_name='estate.property')
    property_title = fields.Char()
    property_buyer = fields.Char()
    visit_time_start = fields.Datetime()
    status = fields.Selection(
        [
            ('scheduled', "Scheduled"),
            ('finished', "Finished"),
        ],
        required=True, default='scheduled'

    )

    @api.constrains('property_id', 'visit_time_start')
    def _check_visit_time(self):
        for visit in self:
            if visit.visit_time_start:
                after_start_hour = fields.Datetime.add(visit.visit_time_start, hours=1)
                before_start_hour = fields.Datetime.subtract(visit.visit_time_start, hours=1)
                wrong_visit = self.env['estate.property.visit'].search([
                    ('id', '!=', visit.id),
                    ('property_id', '=', visit.property_id.id),
                    ('visit_time_start', '>', before_start_hour),
                    ('visit_time_start', '<', after_start_hour)
                ], limit=1)
                if wrong_visit:
                    raise UserError('Time occupied, please select some other time.')

    def _cron_send_reminder(self):
        now = fields.Datetime.now()
        next = fields.Datetime.add(now, days=1)
        visits = self.search([
            ('status', '=', 'scheduled'),
            ('reminder', '=', False),
            ('visit_time_start', '>=', now),
            ('visit_time_start', '<=', next),
        ])
        for visit in visits:
            visit.message_post(
                body=f"Reminder!! Your visit to Property:{visit.property_title or 'Unknown'} is scheduled at {visit.visit_time_start or 'Unknown'} with {visit.property_buyer or 'Unknown'}",
                message_type='notification',
            )
            visit.reminder = True
