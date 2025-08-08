from odoo import models
from datetime import datetime, time

class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'

    def calendar_verify_availability(self, date_start, date_end):
        """ Verify availability of the partner(s) between 2 datetimes on their calendar.
        We only verify events that are not linked to an appointment type with resources since
        someone could take multiple appointment for multiple resources. The availability of
        resources is managed separately by booking lines (see ``appointment.booking.line`` model)

        :param datetime date_start: beginning of slot boundary. Not timezoned UTC;
        :param datetime date_end: end of slot boundary. Not timezoned UTC;
        """
        all_events = self.env['calendar.event'].search(
            ['&',
            ('partner_ids', 'in', self.ids),
            '&', '&',
            ('show_as', '=', 'busy'),
            ('stop', '>', datetime.combine(date_start, time.min)),
            ('start', '<', datetime.combine(date_end, time.max)),
            ],
            order='start asc',
        )
        events_excluding_appointment_resource = all_events.filtered(lambda ev: ev.appointment_type_id.schedule_based_on != 'resources')
        for event in events_excluding_appointment_resource:
            if event.allday or (event.start < date_end and event.stop > date_start):
                if event.appointment_type_id and event.appointment_type_id.resource_capacity != 'one_booking' and all(user in event.appointment_type_id.staff_user_ids.partner_id for user in self):
                    continue
                if event.attendee_ids.filtered_domain(
                        [('state', '!=', 'declined'),
                        ('partner_id', 'in', self.ids)]
                    ):
                    return False

        return True
