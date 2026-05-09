from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _description = 'estate property views'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    estate_property_id = fields.Many2one('estate.property', readonly=True)
    partner_id = fields.Many2one('res.partner')
    time = fields.Datetime(required=True)
    state = fields.Selection(
        selection=[
            ('scheduled', "Scheduled"),
            ('done', "Done"),
            ('cancelled', "Cancelled")
        ]
    )
    calendar_event_ids = fields.One2many('calendar.event', 'estate_visit_id')

    @api.model_create_multi
    def create(self, vals_list):
        visits = super().create(vals_list)
        for visit in visits:
            self.env['calendar.event'].create({
                'name': "%s Visit by %s" % (visit.estate_property_id.name, visit.partner_id.name),
                'start': visit.time,
                'stop': visit.time + timedelta(hours=1),
                'estate_visit_id': visit.id,
                'estate_property_id': visit.estate_property_id.id
            })
        return visits

    @api.constrains('time', 'estate_property_id')
    def _check_time_overlap(self):
        for record in self:

            slot_start = record.time
            slot_end = record.time + timedelta(hours=1)

            overlapping = self.search([
                ('id', '!=', record.id),
                ('estate_property_id', '=', record.estate_property_id.id),
                ('time', '>', slot_start - timedelta(hours=1)),
                ('time', '<', slot_end),
            ])

            if overlapping:
                raise ValidationError(
                    "This time slot is already booked. "
                )

    def action_open_calendar(self):
        calendar_event = self.calendar_event_ids[:1]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit Calendar',
            'res_model': 'calendar.event',
            'res_id': calendar_event.id,
            'view_mode': 'form',
            'view_id': self.env.ref('calendar.view_calendar_event_form').id,
            'target': 'current',
            'context': {'create': False}
        }

    @api.model
    def _cron_notify_salesperson(self):
        now = fields.Datetime.now()
        upcoming_visits = self.search([
            ('time', '>', now),
            ('time', '<', now + timedelta(hours=24)),
            ('state', '=', 'scheduled')
        ])
        for visit in upcoming_visits:
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get_id('estate.property.visit'),
                'res_id': visit.id,
                'user_id': visit.estate_property_id.salesperson_id.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': 'You have a meeting with %s for %s property visit' % (
                        visit.partner_id.name, visit.estate_property_id.name
                ),
                'summary': "%s Visit by %s" % (
                    visit.estate_property_id.name, visit.partner_id.name
                ),
                'automated': True,
            })
        return True
