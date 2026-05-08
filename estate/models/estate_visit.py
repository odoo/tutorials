import logging
from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class EstateVisit(models.Model):
    _name = 'estate.visit'
    _rec_name = 'property_id'
    _inherit = ['mail.thread']

    property_id = fields.Many2one('estate.property', string='Property', required=True)
    visitor_id = fields.Many2one('res.partner', string='Visitor', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', compute='_compute_end_time', store=True)
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='scheduled', required=True)
    notes = fields.Text(string='Notes')
    salesperson_id = fields.Many2one('res.users', string='Salesperson',
                                     default=lambda self: self.env.user)

    reminder_sent = fields.Boolean(default=False)

    @api.depends('start_time')
    def _compute_end_time(self):
        for visit in self:
            if visit.start_time:
                visit.end_time = visit.start_time + timedelta(hours=1)

    @api.constrains('property_id', 'start_time', 'end_time')
    def _check_visit_time(self):
        for visit in self:
            overlapping_visit = self.search([
                ('property_id', '=', visit.property_id.id),
                ('status', '=', 'scheduled'),
                ('id', '!=', visit.id),

                ('start_time', '<', visit.end_time),
                ('end_time', '>', visit.start_time),
            ], limit=1)

            if overlapping_visit:
                raise ValidationError(
                    "Another visit is already scheduled during this time."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            start_time = vals.get('start_time')
            if start_time:
                start_time = fields.Datetime.from_string(start_time)
                if start_time < fields.Datetime.now():
                    raise ValidationError(
                        "Start time must be in the future."
                    )
        return super().create(vals_list)

    @api.model
    def send_visit_reminder(self):
        _logger.info("------------ Visit reminder cron started------------")
        now = fields.Datetime.now()
        next_hour = now + timedelta(hours=1)

        visits = self.search([
            ('status', '=', 'scheduled'),
            ('reminder_sent', '=', False),
            ('start_time', '>=', now),
            ('start_time', '<=', next_hour),
        ])
        template = self.env.ref('estate.email_template_visit_reminder')

        for visit in visits:
            ctx = {
                'sales_person': visit.salesperson_id.name,
                'property_name': visit.property_id.name,
                'custom_message': 'Your property visit is scheduled within the next hour.',
                'start_time': visit.start_time,
                'end_time': visit.end_time
            }
            template.with_context(ctx).send_mail(
                visit.id,
                email_values={
                    'email_to': 'vivah@odoo.com',
                    'email_from': visit.salesperson_id.email,
                },
                force_send=True
            )
            visit.reminder_sent = True
        # template.send_mail(
        #     visit.id,
        #     email_values={
        #         'email_to': 'vivah@odoo.com',
        #         'email_from': 'vivah@odoo.com',
        #     },
        #     force_send=True
        # )
        # visit.reminder_sent = True
        _logger.info("=================Visit reminder cron FINSH=====")
