from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EstatePropertyVisit(models.Model):

    _name = 'estate.property.visit'
    _description = "A  model where visit for the properties are stored"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    property_id = fields.Many2one(
        'estate.property', required=True)
    state = fields.Selection(selection=[('pending', "Pending"),
                                        ('success', "Success"),
                                        ('canceled', "Canceled")],
                             default='pending')
    visitor_id = fields.Many2one(
        'res.partner', required=True, string="Visitor")
    agent_id = fields.Many2one(
        'res.users', ondelete='restrict', string="Agent"
    )
    scheduled_on = fields.Datetime(
        string="Visit Time")
    rating = fields.Integer(string="Rating")
    visits = fields.Integer(string="Visits")

    duration = fields.Datetime(
        string="Visit End")

    @api.onchange('scheduled_on', 'duration')
    def _onchange_scheduled_on(self):
        for rec in self:
            visit_start_time = rec.scheduled_on or fields.Date.context_today(
                self)
            rec.duration = fields.Date.add(visit_start_time, minutes=60)

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            property_id = vals.get('property_id')

            if property_id:
                scheduled_on = fields.Datetime.to_datetime(
                    vals.get('scheduled_on')
                )

                duration = fields.Datetime.to_datetime(
                    vals.get('duration')
                )

                domain = [
                    ('property_id', '=', property_id),
                    ('scheduled_on', '<=', duration),
                    ('duration', '>=', scheduled_on),
                ]

                overlap = self.env['estate.property.visit'].search(
                    domain,
                    limit=1,
                )

                if scheduled_on and scheduled_on < fields.Datetime.now():
                    raise UserError(_(
                        "Visitor cannot be time traveller"
                    ))

                if overlap:
                    raise UserError(_(
                        "Occupied"
                    ))

        return super().create(vals_list)

    @api.model
    def _cron_daily_reminder_send(self):
        now = fields.Datetime.now()
        tomorrow_start = fields.Date.add(now, days=1)
        tomorrow_end = fields.Date.add(now, days=2)
        visits = self.env['estate.property.visit'].search([
            ('scheduled_on', '>=', tomorrow_start),
            ('scheduled_on', '<', tomorrow_end),
            ('state', '=', 'pending'),
        ])

        if not visits:
            _logger.warning("No Visits found: ")
            return

        for visit in visits:
            # breakpoint()
            # visit.message_post(
            #     body=_(
            #         "Reminder: your visit is scheduled tomorrow at %s") % visit.scheduled_on,
            #     partner_ids=[visit.visitor_id.id],   # who gets notified
            #     message_type='notification',
            #     subtype_xmlid=None,
            # )
            visit.activity_schedule(
                activity_type_id=15,
                summary='Visit Schedules',
                note=_("Visit scheduled tomorrow at %s") % visit.scheduled_on,
                date_deadline=visit.scheduled_on.date(),
                user_id=visit.agent_id.id,   # assign to the agent
            )
