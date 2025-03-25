from odoo import fields,models

class CalenderEventInhrited(models.Model):
    _inherit = 'calendar.event'

    appointment_type_manage_capacity = fields.Selection(related="appointment_type_id.resource_capacity")
    
    def _has_conflicting_events(self, other_events):
        self.ensure_one()

        if self.appointment_type_id.resource_capacity != 'one_booking' and other_events:
            # Avoid checking events related to the same appointment type and having multiple seats/bookings per slot
            other_events = other_events.filtered(lambda event: event.appointment_type_id != self.appointment_type_id)

        return other_events

    def _inverse_resource_ids_or_capacity(self):
        """Update booking lines as inverse of both resource capacity and resource_ids.

        As both values are related to the booking line and resource capacity is dependant
        on resources existing in the first place. They need to both use the same inverse
        field to ensure there is no ordering conflict.
        """
        booking_lines = []
        for event in self:
            resources = event.resource_ids
            if resources:
                # Ignore the inverse and keep the previous booking lines when we duplicate an event
                if self.env.context.get('is_appointment_copied'):
                    continue
                if event.appointment_type_manage_capacity != 'one_booking' and self.resource_total_capacity_reserved:
                    capacity_to_reserve = self.resource_total_capacity_reserved
                else:
                    capacity_to_reserve = sum(event.booking_line_ids.mapped('capacity_reserved')) or sum(resources.mapped('capacity'))
                event.booking_line_ids.sudo().unlink()
                for resource in resources.sorted("shareable"):
                    if event.appointment_type_manage_capacity != 'one_booking' and capacity_to_reserve <= 0:
                        break
                    booking_lines.append({
                        'appointment_resource_id': resource.id,
                        'calendar_event_id': event.id,
                        'capacity_reserved': min(resource.capacity, capacity_to_reserve),
                    })
                    capacity_to_reserve -= min(resource.capacity, capacity_to_reserve)
                    capacity_to_reserve = max(0, capacity_to_reserve)
            else:
                event.booking_line_ids.sudo().unlink()
        self.env['appointment.booking.line'].sudo().create(booking_lines)
