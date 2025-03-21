from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    appointment_type_capacity_type = fields.Selection(related="appointment_type_id.capacity_type")
 
    # @api.model
    # def create(self, vals_list):
    #     """ Ensure that booking respects capacity rules """
    #     appointment_type = self.env["appointment.type"].browse(vals_list.get("appointment_type_id"))
    #     print()
    #     if appointment_type.capacity_type in ["multiple_bookings", "multiple_seats"]:
    #         if appointment_type.available_capacity <= 0:
    #             raise ValidationError("This time slot is fully booked.")
    #         print(appointment_type.available_capacity)
    #         appointment_type.available_capacity -= vals_list.get("capacity_reserved") or 1 # Reduce available slots
    #         print(appointment_type.available_capacity)

        # return super(CalendarEvent, self).create(vals_list)
    @api.depends('appointment_type_capacity_type', 'resource_total_capacity_reserved')
    def _inverse_resource_ids_or_capacity(self):
        booking_lines = []
        for event in self:
            resources = event.resource_ids
            if resources:
                # Ignore the inverse and keep the previous booking lines when we duplicate an event
                if self.env.context.get('is_appointment_copied'):
                    continue
                if event.appointment_type_manage_capacity != 'single_bookings' and self.resource_total_capacity_reserved:
                    capacity_to_reserve = self.resource_total_capacity_reserved
                else:
                    capacity_to_reserve = sum(event.booking_line_ids.mapped('capacity_reserved')) or sum(resources.mapped('capacity'))
                event.booking_line_ids.sudo().unlink()
                for resource in resources.sorted("shareable"):
                    if event.appointment_type_manage_capacity != 'single_bookings' and capacity_to_reserve <= 0:
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
