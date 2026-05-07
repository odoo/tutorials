import logging

from odoo import fields, models, api
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class EstatePropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _inherit = ['mail.thread']
    _description = 'Visits scheduled for the property'
    _rec_name = 'property_title'

    finished = fields.Boolean(default=True)
    reminder = fields.Boolean(default=False)
    property_id = fields.Many2one(comodel_name='estate.properties')
    property_title = fields.Char()
    property_buyer = fields.Char()
    visit_time_start = fields.Datetime()
    visit_time_end = fields.Datetime(compute='_compute_visit_end_time', store=True)
    status = fields.Selection(
        [
            ('scheduled', "Scheduled"),
            ('finished', "Finished"),
        ],
        required=True, default='scheduled'

    )

    @api.depends('visit_time_start')
    def _compute_visit_end_time(self):
        for visit in self:
            if visit.visit_time_start:
                visit.visit_time_end = fields.Datetime.add(visit.visit_time_start, hours=1)
            else:
                visit.visit_time_end = False

    @api.constrains('property_id', 'visit_time_start', 'visit_time_end')
    def _check_visit_time(self):
        for visit in self:
            if visit.visit_time_end and visit.visit_time_start:
                _logger.error("FOUND DA TIME")
                if visit.visit_time_start > visit.visit_time_end:
                    raise UserError("Start time cannot be after end time")
                wrong_visit = self.env['estate.property.visit'].search([
                    ('id', '!=', visit.id), # Use visit.id
                    ('property_id', '=', visit.property_id.id), # Use visit.property_id.id
                    ('visit_time_start', '<', visit.visit_time_end),
                    ('visit_time_end', '>', visit.visit_time_start)
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
        if visits:
            for visit in visits:
                visit.message_post(
                    body="Reminder",
                    message_type='notification',
                )
                visit.status = 'finished'
            
        _logger.info("Cron duration = %d seconds" % ((fields.Datetime.now() - now).total_seconds()))

