from odoo import models, Command


class CalendarBookingLine(models.Model):
    _inherit = 'calendar.booking'
    _description = "Meeting Booking"

    def _make_event_from_paid_booking(self):
        """ This method is called when the booking is considered as paid. We create a calendar event from the booking values. """
        if not self:
            return
        todo = self.filtered(lambda booking: not booking.calendar_event_id)
        unavailable_bookings = todo._filter_unavailable_bookings()

        for booking in todo - unavailable_bookings:
            booking_line_values = [{
                'appointment_user_id': line.appointment_user_id.id,
                'appointment_resource_id': line.appointment_resource_id.id,
                'capacity_reserved': line.capacity_reserved,
                'capacity_used': line.capacity_used,
            } for line in booking.booking_line_ids]

            calendar_event_values = booking.appointment_type_id._prepare_calendar_event_values(
                booking.asked_capacity, booking_line_values, booking.duration, booking.appointment_invite_id,
                booking.guest_ids, booking.name, booking.partner_id, booking.staff_user_id, booking.start, booking.stop
            )
            calendar_event_values['appointment_answer_input_ids'] = [Command.set(booking.appointment_answer_input_ids.ids)]

            meeting = self.env['calendar.event'].with_context(
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notify_author=True,
                allowed_company_ids=booking.staff_user_id.company_ids.ids,
            ).sudo().create(calendar_event_values)
            booking.calendar_event_id = meeting

        unavailable_bookings.not_available = True
        unavailable_bookings._log_booking_collisions()
