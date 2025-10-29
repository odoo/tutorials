from odoo import models, fields


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    appointment_type_capacity_type = fields.Selection(related="appointment_type_id.capacity_type")

    def _inverse_resource_ids_or_capacity(self):
        booking_lines = []
        booking_lines_to_delete = self.env['appointment.booking.line']
        for event in self:
            resources = event.resource_ids
            if resources:
                # Ignore the inverse and keep the previous booking lines when we duplicate an event
                if self.env.context.get('is_appointment_copied'):
                    continue
                if event.appointment_type_capacity_type != 'one_booking' and event.resource_total_capacity_reserved:
                    capacity_to_reserve = event.resource_total_capacity_reserved
                else:
                    capacity_to_reserve = sum(event.booking_line_ids.mapped('capacity_reserved')) or sum(resources.mapped('capacity'))
                booking_lines_to_delete |= event.booking_line_ids
                for resource in resources.sorted("shareable"):
                    if event.appointment_type_capacity_type != 'one_booking' and capacity_to_reserve <= 0:
                        break
                    booking_lines.append({
                        'appointment_resource_id': resource.id,
                        'calendar_event_id': event.id,
                        'capacity_reserved': min(resource.capacity, capacity_to_reserve),
                    })
                    capacity_to_reserve -= min(resource.capacity, capacity_to_reserve)
                    capacity_to_reserve = max(0, capacity_to_reserve)
            else:
                booking_lines_to_delete |= event.booking_line_ids
        booking_lines_to_delete.unlink()
        self.env['appointment.booking.line'].sudo().create(booking_lines)
