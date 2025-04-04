import calendar as cal
import random
import pytz
from datetime import datetime,time
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from babel.dates import format_datetime, format_time
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.tools.misc import babel_locale_parse, get_lang

class AppointmentType(models.Model):
    _inherit = "appointment.type"

    track_capacity = fields.Selection(
        [
            ("one_booking_per_slot", "One Booking Per Slot"),
            ("multiple_booking_per_slot", "Multiple Booking Per Slot"),
            ("multiple_seat_per_slot", "Multiple Seat Per Slot"),
        ],
        string="Capacities",
        store=True,
        default="one_booking_per_slot",
        required=True,
        readonly=False,
        help="""Manage the maximum number of bookings that seats and resources can handle. "One booking per slot" means each user can book a slot exclusively, 
while "multiple bookings per slot" allows multiple bookings based on user input. 
"Multiple seat per slot" indicates that bookings can be made according to the user's capacity.""",
    )
    total_booking = fields.Integer("Total Booking", default=1)

    _sql_constraints = [
        ("check_total_booking", "CHECK(total_booking >= 1)", "total booking/seats should be at least 1."),
    ]

    @api.onchange("track_capacity")
    def _onchange_track_capacity(self):
        if (self.track_capacity == "one_booking_per_slot"):
            self.resource_manage_capacity = False
        else:
            self.resource_manage_capacity = True

    # --------------------------------------
    # resources - Slots Availability
    # --------------------------------------

    def _slot_availability_is_resource_available(self, slot, resource, availability_values):
        result = super()._slot_availability_is_resource_available(slot,resource, availability_values)

        slot_start_dt_utc, slot_end_dt_utc = slot['UTC'][0], slot['UTC'][1]
        resource_to_bookings = availability_values.get('resource_to_bookings')

        if resource_to_bookings.get(resource):
            if resource_to_bookings[resource].filtered(lambda bl: bl.event_start < slot_end_dt_utc and bl.event_stop > slot_start_dt_utc):
                # my code changes
                if self.track_capacity == "multiple_booking_per_slot":
                    result = True
                elif self.track_capacity == "multiple_seat_per_slot":
                    result = resource.shareable
        return result

    # --------------------------------------
    # Users - Slots Availability
    # --------------------------------------

    def _get_users_remaining_capacity(self, users, slot_start_utc, slot_stop_utc, filter_users=None):

        self.ensure_one()

        all_users = users & self.staff_user_ids
        if filter_users:
            all_users &= filter_users
        if not all_users:
            return {'total_remaining_capacity': 0}

        booking_lines = self.env['appointment.booking.line'].sudo().search([
            ('appointment_user_id', 'in', all_users.ids),
            ('event_start', '<', slot_stop_utc),
            ('event_stop', '>', slot_start_utc),
        ])

        users_booking_lines = booking_lines.grouped('appointment_user_id')

        users_remaining_capacity = {
            user: self.total_booking - sum(booking_line.capacity_used for booking_line in users_booking_lines.get(user, []))
            for user in all_users
        }

        # Calculate total remaining capacity across all users
        users_remaining_capacity.update(total_remaining_capacity=sum(users_remaining_capacity.values()))
        return users_remaining_capacity

    # add asked_capacity parameter
    def _slots_fill_users_availability(self, slots, start_dt, end_dt, filter_users=None, asked_capacity=1):

        available_users = [
            user.with_context(tz=user.tz)
            for user in (filter_users or self.staff_user_ids)
        ]
        random.shuffle(available_users)
        available_users_tz = self.env['res.users'].concat(*available_users)

        # fetch value used for availability in batch
        availability_values = self._slot_availability_prepare_users_values(
            available_users_tz, start_dt, end_dt
        )

        for slot in slots:
            if self.assign_method == 'time_resource':
                available_staff_users = available_users_tz.filtered(
                    lambda staff_user: self._slot_availability_is_user_available(
                        slot,
                        staff_user,
                        availability_values,
                        asked_capacity
                    )
                )
            else:
                available_staff_users = next(
                    (staff_user for staff_user in available_users_tz if self._slot_availability_is_user_available(
                        slot,
                        staff_user,
                        availability_values,
                        asked_capacity
                    )),
                    False)
            if available_staff_users:
                if self.assign_method == 'time_resource':
                    slot['available_staff_users'] = available_staff_users
                else:
                    slot['staff_user_id'] = available_staff_users

    # add asked capacity
    def _slot_availability_is_user_available(self, slot, staff_user, availability_values, asked_capacity=1):

        slot_start_dt_utc, slot_end_dt_utc = slot['UTC'][0], slot['UTC'][1]
        staff_user_tz = pytz.timezone(staff_user.tz) if staff_user.tz else pytz.utc
        slot_start_dt_user_timezone = slot_start_dt_utc.astimezone(staff_user_tz)
        slot_end_dt_user_timezone = slot_end_dt_utc.astimezone(staff_user_tz)

        if slot['slot'].restrict_to_user_ids and staff_user not in slot['slot'].restrict_to_user_ids:
            return False
        users_remaining_capacity = self._get_users_remaining_capacity(staff_user, slot['UTC'][0], slot['UTC'][1])
        partner_to_events = availability_values.get('partner_to_events') or {}
        if partner_to_events.get(staff_user.partner_id):
            for day_dt in rrule.rrule(freq=rrule.DAILY,
                                      dtstart=slot_start_dt_utc,
                                      until=slot_end_dt_utc,
                                      interval=1):
                day_events = partner_to_events[staff_user.partner_id].get(day_dt.date()) or []
                for event in day_events:
                    if not event.allday and (event.start < slot_end_dt_utc and event.stop > slot_start_dt_utc):
                        # my code changes
                        if self.track_capacity != 'one_booking_per_slot' and users_remaining_capacity['total_remaining_capacity'] >= asked_capacity:
                            continue
                        return False
            for day_dt in rrule.rrule(freq=rrule.DAILY,
                                      dtstart=slot_start_dt_user_timezone,
                                      until=slot_end_dt_user_timezone,
                                      interval=1):
                day_events = partner_to_events[staff_user.partner_id].get(day_dt.date()) or []
                if any(event.allday for event in day_events):
                    return False
        return True

    def _get_appointment_slots(self, timezone, filter_users=None, filter_resources=None, asked_capacity=1, reference_date=None):

        self.ensure_one()

        if not self.active:
            return []
        now = datetime.utcnow()
        if not reference_date:
            reference_date = now

        try:
            requested_tz = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            requested_tz = self.appointment_tz

        appointment_duration_days = self.max_schedule_days
        unique_slots = self.slot_ids.filtered(lambda slot: slot.slot_type == 'unique')

        if self.category == 'custom' and unique_slots:
            # Custom appointment type, the first day should depend on the first slot datetime
            start_first_slot = unique_slots[0].start_datetime
            first_day_utc = start_first_slot if reference_date > start_first_slot else reference_date
            first_day = requested_tz.fromutc(first_day_utc + relativedelta(hours=self.min_schedule_hours))
            appointment_duration_days = (unique_slots[-1].end_datetime.date() - reference_date.date()).days
            last_day = requested_tz.fromutc(reference_date + relativedelta(days=appointment_duration_days))
        elif self.category == 'punctual':
            # Punctual appointment type, the first day is the start_datetime if it is in the future, else the first day is now
            first_day = requested_tz.fromutc(self.start_datetime if self.start_datetime > now else now)
            last_day = requested_tz.fromutc(self.end_datetime)
        else:
            # Recurring appointment type
            first_day = requested_tz.fromutc(reference_date + relativedelta(hours=self.min_schedule_hours))
            last_day = requested_tz.fromutc(reference_date + relativedelta(days=appointment_duration_days))

        # Compute available slots (ordered)
        slots = self._slots_generate(
            first_day.astimezone(pytz.utc),
            last_day.astimezone(pytz.utc),
            timezone,
            reference_date=reference_date
        )

        # No slots -> skip useless computation
        if not slots:
            return slots
        valid_users = filter_users.filtered(lambda user: user in self.staff_user_ids) if filter_users else None
        valid_resources = filter_resources.filtered(lambda resource: resource in self.resource_ids) if filter_resources else None
        # Not found staff user : incorrect configuration -> skip useless computation
        if filter_users and not valid_users:
            return []
        if filter_resources and not valid_resources:
            return []
        # Used to check availabilities for the whole last day as _slot_generate will return all slots on that date.
        last_day_end_of_day = datetime.combine(
            last_day.astimezone(pytz.timezone(self.appointment_tz)),
            time.max
        )
        if self.schedule_based_on == 'users':
            self._slots_fill_users_availability(
                slots,
                first_day.astimezone(pytz.UTC),
                last_day_end_of_day.astimezone(pytz.UTC),
                valid_users,
                asked_capacity
            )
            slot_field_label = 'available_staff_users' if self.assign_method == 'time_resource' else 'staff_user_id'
        else:
            self._slots_fill_resources_availability(
                slots,
                first_day.astimezone(pytz.UTC),
                last_day_end_of_day.astimezone(pytz.UTC),
                valid_resources,
                asked_capacity,
            )
            slot_field_label = 'available_resource_ids'

        total_nb_slots = sum(slot_field_label in slot for slot in slots)
        # If there is no slot for the minimum capacity then we return an empty list.
        # This will lead to a screen informing the customer that there is no availability.
        # We don't want to return an empty list if the capacity as been tempered by the customer
        # as he should still be able to interact with the screen and select another capacity.
        if not total_nb_slots and asked_capacity == 1:
            return []
        nb_slots_previous_months = 0

        # Compute calendar rendering and inject available slots
        today = requested_tz.fromutc(reference_date)
        start = slots[0][timezone][0] if slots else today
        locale = babel_locale_parse(get_lang(self.env).code)
        month_dates_calendar = cal.Calendar(locale.first_week_day).monthdatescalendar
        months = []
        while (start.year, start.month) <= (last_day.year, last_day.month):
            nb_slots_next_months = sum(slot_field_label in slot for slot in slots)
            has_availabilities = False
            dates = month_dates_calendar(start.year, start.month)
            for week_index, week in enumerate(dates):
                for day_index, day in enumerate(week):
                    mute_cls = weekend_cls = today_cls = None
                    today_slots = []
                    if day.weekday() in (locale.weekend_start, locale.weekend_end):
                        weekend_cls = 'o_weekend bg-light'
                    if day == today.date() and day.month == today.month:
                        today_cls = 'o_today'
                    if day.month != start.month:
                        mute_cls = 'd-none'
                    else:
                        # slots are ordered, so check all unprocessed slots from until > day
                        while slots and (slots[0][timezone][0].date() <= day):
                            if (slots[0][timezone][0].date() == day) and (slot_field_label in slots[0]):
                                slot_start_dt_tz = slots[0][timezone][0].strftime('%Y-%m-%d %H:%M:%S')
                                slot = {
                                    'datetime': slot_start_dt_tz,
                                    'available_resources': [{
                                        'id': resource.id,
                                        'name': resource.name,
                                        'capacity': resource.capacity,
                                    } for resource in slots[0]['available_resource_ids']] if self.schedule_based_on == 'resources' else False,
                                }
                                if self.schedule_based_on == 'users' and self.assign_method == 'time_resource':
                                    slot.update({'available_staff_users': [{
                                        'id': staff.id,
                                        'name': staff.name,
                                    } for staff in slots[0]['available_staff_users']]})
                                elif self.schedule_based_on == 'users':
                                    slot.update({'staff_user_id': slots[0]['staff_user_id'].id})
                                if slots[0]['slot'].allday:
                                    slot_duration = 24
                                    slot.update({
                                        'hours': _("All day"),
                                        'slot_duration': slot_duration,
                                    })
                                else:
                                    start_hour = format_time(slots[0][timezone][0].time(), format='short', locale=locale)
                                    end_hour = format_time(slots[0][timezone][1].time(), format='short', locale=locale) if self.category == 'custom' else False
                                    slot_duration = str((slots[0][timezone][1] - slots[0][timezone][0]).total_seconds() / 3600)
                                    slot.update({
                                        'start_hour': start_hour,
                                        'end_hour': end_hour,
                                        'slot_duration': slot_duration,
                                    })
                                url_parameters = {
                                    'date_time': slot_start_dt_tz,
                                    'duration': slot_duration,
                                }
                                if self.schedule_based_on == 'users' and self.assign_method != 'time_resource':
                                    url_parameters.update(staff_user_id=str(slots[0]['staff_user_id'].id))
                                elif self.schedule_based_on == 'resources':
                                    url_parameters.update(available_resource_ids=str(slots[0]['available_resource_ids'].ids))
                                slot['url_parameters'] = url_encode(url_parameters)
                                today_slots.append(slot)
                                nb_slots_next_months -= 1
                            slots.pop(0)
                    today_slots = sorted(today_slots, key=lambda d: d['datetime'])
                    dates[week_index][day_index] = {
                        'day': day,
                        'slots': today_slots,
                        'mute_cls': mute_cls,
                        'weekend_cls': weekend_cls,
                        'today_cls': today_cls
                    }

                    has_availabilities = has_availabilities or bool(today_slots)

            months.append({
                'id': len(months),
                'month': format_datetime(start, 'MMMM Y', locale=get_lang(self.env).code),
                'weeks': dates,
                'has_availabilities': has_availabilities,
                'nb_slots_previous_months': nb_slots_previous_months,
                'nb_slots_next_months': nb_slots_next_months,
            })
            nb_slots_previous_months = total_nb_slots - nb_slots_next_months
            start = start + relativedelta(months=1)
        return months
