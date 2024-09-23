from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class RoomBooking(models.Model):
    _inherit = 'room.booking'

    task_ids = fields.Many2many('project.task', string='Select Tasks')
    label = fields.Text(string='Label', compute='_compute_label')

    @api.constrains("start_datetime", "stop_datetime")
    def _check_unique_slot(self):
        for booking in self:
            day_start = booking.start_datetime.replace(hour=0, minute=0, second=0)
            day_end = booking.start_datetime.replace(hour=23, minute=59, second=59)

            conflicting_bookings = self.search([
                ("room_id", "=", booking.room_id.id),
                ("id", "!=", booking.id),
                ("start_datetime", ">=", day_start),
                ("stop_datetime", "<=", day_end)
            ], order="start_datetime asc")

            available_slots = [(day_start, day_end)]

            for event in conflicting_bookings:
                new_slots = []
                for slot_start, slot_end in available_slots:
                    if event.start_datetime > slot_start and event.stop_datetime < slot_end:
                        if event.start_datetime - slot_start > timedelta(minutes=1):
                            new_slots.append((slot_start, event.start_datetime))
                        if slot_end - event.stop_datetime > timedelta(minutes=1):
                            new_slots.append((event.stop_datetime, slot_end))
                    elif event.start_datetime <= slot_start < event.stop_datetime:
                        if slot_end - event.stop_datetime > timedelta(minutes=1):
                            new_slots.append((event.stop_datetime, slot_end))
                    elif event.start_datetime < slot_end <= event.stop_datetime:
                        if event.start_datetime - slot_start > timedelta(minutes=1):
                            new_slots.append((slot_start, event.start_datetime))
                    else:
                        new_slots.append((slot_start, slot_end)) 
                available_slots = new_slots

            print(available_slots)

            if not available_slots:
                raise UserError(_(
                    "Room %(room_name)s is fully booked for the day. No available slots.",
                    room_name=booking.room_id.name
                ))

            for slot_start, slot_end in available_slots:
                if slot_start <= booking.start_datetime and slot_end >= booking.stop_datetime:
                    break
            else:
                for i in available_slots:
                    if i[0] > booking.start_datetime:
                        next_available_slot = i
                        break
                raise UserError(_(
                    "Room %(room_name)s is already booked during the selected time slot. "
                    "The next available slot is %(next_available_start)s - %(next_available_end)s.",
                    room_name=booking.room_id.name,
                    next_available_start=(next_available_slot[0] + timedelta(hours=5, minutes=29, seconds=59) if next_available_slot[0] + timedelta(hours=5, minutes=29, seconds=59) < day_end else day_start).strftime('%H:%M:%S'),
                    next_available_end=(day_end if (next_available_slot[1] + timedelta(hours=5, minutes=29, seconds=59)) > day_end else next_available_slot[1] + timedelta(hours=5, minutes=29, seconds=59)).strftime('%H:%M:%S')
                ))

            if booking.start_datetime >= booking.stop_datetime:
                raise UserError(_(
                    "The start time must be earlier than the end time for booking %(booking_name)s.",
                    booking_name=booking.name
                ))


