from datetime import datetime, time

from odoo import models


class Partner(models.Model):
    _inherit = "res.partner"

    def calendar_verify_availability(self, date_start, date_end):
        """Check if the user is available based on their appointment type."""
        all_events = self.env["calendar.event"].search(
            [
                "&",
                ("partner_ids", "in", self.ids),
                "&",
                "&",
                ("show_as", "=", "busy"),
                ("stop", ">", datetime.combine(date_start, time.min)),
                ("start", "<", datetime.combine(date_end, time.max)),
            ],
            order="start asc",
        )
        # Exclude events linked to appt types that are based on resources
        events_excluding_appointment_resource = all_events.filtered(
            lambda ev: ev.appointment_type_id.schedule_based_on != "resources"
        )

        for event in events_excluding_appointment_resource:
            if event.allday or (event.start < date_end and event.stop > date_start):
                appointment_type = event.appointment_type_id

                if appointment_type and appointment_type.capacity_type != "one_booking":
                    staff_user = event.user_id
                    if not staff_user:
                        return False

                    remaining_capacity = appointment_type._get_user_remaining_capacity(
                        event.user_id, date_start, date_end
                    )

                    # Determine required capacity
                    required_capacity = self.env.context.get("asked_capacity", 1)
                    if remaining_capacity >= required_capacity:
                        continue

                # check if user is already booked in this slot
                if event.attendee_ids.filtered_domain(
                    [("state", "!=", "declined"), ("partner_id", "in", self.ids)]
                ):
                    return False

        return True
