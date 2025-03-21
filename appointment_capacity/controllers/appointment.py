
import json
import pytz
import re

from pytz.exceptions import UnknownTimeZoneError

from babel.dates import format_datetime, format_date, format_time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from markupsafe import Markup
from urllib.parse import unquote_plus
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_encode

from odoo import Command, exceptions, http, fields, _
from odoo.http import request, route
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dtf, email_normalize
from odoo.tools.mail import is_html_empty
from odoo.tools.misc import babel_locale_parse, get_lang
from odoo.addons.base.models.ir_qweb import keep_query
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.phone_validation.tools import phone_validation
from odoo.exceptions import UserError

from odoo.addons.appointment.controllers.appointment import AppointmentController


class AppointmentCapacityController(AppointmentController):
    # pass


    def _prepare_appointment_type_page_values(self, appointment_type, staff_user_id=False, resource_selected_id=False, **kwargs):
        """ Computes all values needed to choose between / common to all appointment_type page templates.

        :return: a dict containing:
            - available_appointments: all available appointments according to current filters and invite tokens.
            - filter_appointment_type_ids, filter_staff_user_ids and invite_token parameters.
            - user_default: the first of possible staff users. It will be selected by default (in the user select dropdown)
            if no user_selected. Otherwise, the latter will be preselected instead. It is only set if there is at least one
            possible user and the choice is activated in appointment_type, or used for having the user name in title if there
            is a single possible user, for random selection.
            - user_selected: the user corresponding to staff_user_id in the url and to the selected one. It can be selected
            upstream, from the operator_select screen (see WebsiteAppointment controller), or coming back from an error.
            It is only set if among the possible users.
            - users_possible: all possible staff users considering filter_staff_user_ids and staff members of appointment_type.
            - resource_selected: the resource corresponding to resource_selected_id in the url and to the selected one. It can be selected
            upstream, from the operator_select screen (see WebsiteAppointment controller), or coming back from an error.
            - resources_possible: all possible resources considering filter_resource_ids and resources of appointment type.
            - max_capacity: the maximum capacity that can be selected by the user to make an appointment on a resource.
            - hide_select_dropdown: True if the user select dropdown should be hidden. (e.g. an operator has been selected before)
            Even if hidden, it can still be in the view and used to update availabilities according to the selected user in the js.
        """
        filter_staff_user_ids = json.loads(kwargs.get('filter_staff_user_ids') or '[]')
        filter_resource_ids = json.loads(kwargs.get('filter_resource_ids') or '[]')
        users_possible = self._get_possible_staff_users(appointment_type, filter_staff_user_ids)
        resources_possible = self._get_possible_resources(appointment_type, filter_resource_ids)
        user_default = user_selected = request.env['res.users']
        resource_default = resource_selected = request.env['appointment.resource']
        staff_user_id = int(staff_user_id) if staff_user_id else False
        resource_selected_id = int(resource_selected_id) if resource_selected_id else False

        if appointment_type.schedule_based_on == 'users':
            if appointment_type.assign_method == 'resource_time' and users_possible:
                if staff_user_id and staff_user_id in users_possible.ids:
                    user_selected = request.env['res.users'].sudo().browse(staff_user_id)
                user_default = users_possible[0]
            elif appointment_type.assign_method == 'time_auto_assign' and len(users_possible) == 1:
                user_default = users_possible[0]
        elif resources_possible:
            if resource_selected_id and resource_selected_id in resources_possible.ids and appointment_type.assign_method != 'time_resource':
                resource_selected = request.env['appointment.resource'].sudo().browse(resource_selected_id)
            elif appointment_type.assign_method == 'resource_time':
                resource_default = resources_possible[0]
        
        capacity_type = appointment_type.capacity_type
        if capacity_type == 'multiple_seats':
            if appointment_type.schedule_based_on == 'users':
                max_capacity_possible = appointment_type.user_capacity_count
            else:
                possible_combinations = (resource_selected or resource_default or resources_possible)._get_filtered_possible_capacity_combinations(1, {})
                max_capacity_possible = possible_combinations[-1][1] if possible_combinations else 1
        else:
            max_capacity_possible = 1

        return {
            'asked_capacity': int(kwargs['asked_capacity']) if kwargs.get('asked_capacity') else False,
            'available_appointments': kwargs['available_appointments'],
            'filter_appointment_type_ids': kwargs.get('filter_appointment_type_ids'),
            'filter_staff_user_ids': kwargs.get('filter_staff_user_ids'),
            'filter_resource_ids': kwargs.get('filter_resource_ids'),
            'hide_select_dropdown': len(users_possible if appointment_type.schedule_based_on == 'users' else resources_possible) <= 1,
            'invite_token': kwargs.get('invite_token'),
            'max_capacity': min(12, max_capacity_possible),
            'resource_default': resource_default,
            'resource_selected': resource_selected,
            'resources_possible': resources_possible,
            'user_default': user_default,
            'user_selected': user_selected,
            'users_possible': users_possible,
        }



    @http.route()
    def appointment_form_submit(self, appointment_type_id, datetime_str, duration_str, name, phone, email, staff_user_id=None, available_resource_ids=None, asked_capacity=1,
                                guest_emails_str=None, **kwargs):
        """
        Create the event for the appointment and redirect on the validation page with a summary of the appointment.

        :param appointment_type_id: the appointment type id related
        :param datetime_str: the string representing the datetime
        :param duration_str: the string representing the duration
        :param name: the name of the user sets in the form
        :param phone: the phone of the user sets in the form
        :param email: the email of the user sets in the form
        :param staff_user_id: the user selected for the appointment
        :param available_resource_ids: the resources ids available for the appointment
        :param asked_capacity: asked capacity for the appointment
        :param str guest_emails: optional line-separated guest emails. It will
          fetch or create partners to add them as event attendees;
        """
        domain = self._appointments_base_domain(
            filter_appointment_type_ids=kwargs.get('filter_appointment_type_ids'),
            search=kwargs.get('search'),
            invite_token=kwargs.get('invite_token')
        )

        available_appointments = self._fetch_and_check_private_appointment_types(
            kwargs.get('filter_appointment_type_ids'),
            kwargs.get('filter_staff_user_ids'),
            kwargs.get('filter_resource_ids'),
            kwargs.get('invite_token'),
            domain=domain,
        )
        appointment_type = available_appointments.filtered(lambda appt: appt.id == int(appointment_type_id))

        if not appointment_type:
            raise NotFound()
        timezone = request.session.get('timezone') or appointment_type.appointment_tz
        tz_session = pytz.timezone(timezone)
        datetime_str = unquote_plus(datetime_str)
        date_start = tz_session.localize(fields.Datetime.from_string(datetime_str)).astimezone(pytz.utc).replace(tzinfo=None)
        duration = float(duration_str)
        date_end = date_start + relativedelta(hours=duration)
        invite_token = kwargs.get('invite_token')

        staff_user = request.env['res.users']
        resources = request.env['appointment.resource']
        resource_ids = None
        asked_capacity = int(asked_capacity)
        resources_remaining_capacity = None
        users_remaining_capacity = None
        if appointment_type.schedule_based_on == 'resources':
            resource_ids = json.loads(unquote_plus(available_resource_ids))
            # Check if there is still enough capacity (in case someone else booked with a resource in the meantime)
            resources = request.env['appointment.resource'].sudo().browse(resource_ids).exists()
            if any(resource not in appointment_type.resource_ids for resource in resources):
                raise NotFound()
            resources_remaining_capacity = appointment_type._get_resources_remaining_capacity(resources, date_start, date_end, with_linked_resources=False)
            if resources_remaining_capacity['total_remaining_capacity'] < asked_capacity:
                return request.redirect('/appointment/%s?%s' % (appointment_type.id, keep_query('*', state='failed-resource')))
        else:
            # check availability of the selected user again (in case someone else booked while the client was entering the form)
            staff_user = request.env['res.users'].sudo().search([('id', '=', int(staff_user_id))])
            if staff_user not in appointment_type.staff_user_ids:
                raise NotFound()
            if staff_user and not staff_user.partner_id.calendar_verify_availability(date_start, date_end):
                return request.redirect('/appointment/%s?%s' % (appointment_type.id, keep_query('*', state='failed-staff-user')))
            # check if there is still enough capacity
            users_remaining_capacity = appointment_type._get_users_remaining_capacity(staff_user, date_start, date_end)
            if users_remaining_capacity['total_remaining_capacity'] < asked_capacity and appointment_type.capacity_type != 'one_booking':
                return request.redirect('/appointment/%s?%s' % (appointment_type.id, keep_query('*', state='failed-staff-user')))


        guests = None
        if appointment_type.allow_guests:
            if guest_emails_str:
                guests = request.env['calendar.event'].sudo()._find_or_create_partners(guest_emails_str)

        customer = self._get_customer_partner()

        # considering phone and email are mandatory
        new_customer = not (customer.email) or not (customer.phone)
        if not new_customer and customer.email != email and customer.email_normalized != email_normalize(email):
            new_customer = True
        if not new_customer and not customer.phone:
            new_customer = True
        if not new_customer:
            customer_phone_fmt = customer._phone_format(fname="phone")
            input_country = self._get_customer_country()
            input_phone_fmt = phone_validation.phone_format(phone, input_country.code, input_country.phone_code, force_format="E164", raise_exception=False)
            new_customer = customer.phone != phone and customer_phone_fmt != input_phone_fmt

        if new_customer:
            customer = customer.sudo().create({
                'name': name,
                'phone': customer._phone_format(number=phone, country=self._get_customer_country()) or phone,
                'email': email,
                'lang': request.lang.code,
            })

        # partner_inputs dictionary structures all answer inputs received on the appointment submission: key is question id, value
        # is answer id (as string) for choice questions, text input for text questions, array of ids for multiple choice questions.
        partner_inputs = {}
        appointment_question_ids = appointment_type.question_ids.ids
        for k_key, k_value in [item for item in kwargs.items() if item[1]]:
            question_id_str = re.match(r"\bquestion_([0-9]+)\b", k_key)
            if question_id_str and int(question_id_str.group(1)) in appointment_question_ids:
                partner_inputs[int(question_id_str.group(1))] = k_value
                continue
            checkbox_ids_str = re.match(r"\bquestion_([0-9]+)_answer_([0-9]+)\b", k_key)
            if checkbox_ids_str:
                question_id, answer_id = [int(checkbox_ids_str.group(1)), int(checkbox_ids_str.group(2))]
                if question_id in appointment_question_ids:
                    partner_inputs[question_id] = partner_inputs.get(question_id, []) + [answer_id]

        # The answer inputs will be created in _prepare_calendar_event_values from the values in answer_input_values
        answer_input_values = []
        base_answer_input_vals = {
            'appointment_type_id': appointment_type.id,
            'partner_id': customer.id,
        }

        for question in appointment_type.question_ids.filtered(lambda question: question.id in partner_inputs.keys()):
            if question.question_type == 'checkbox':
                answers = question.answer_ids.filtered(lambda answer: answer.id in partner_inputs[question.id])
                answer_input_values.extend([
                    dict(base_answer_input_vals, question_id=question.id, value_answer_id=answer.id) for answer in answers
                ])
            elif question.question_type in ['select', 'radio']:
                answer_input_values.append(
                    dict(base_answer_input_vals, question_id=question.id, value_answer_id=int(partner_inputs[question.id]))
                )
            elif question.question_type in ['char', 'text']:
                answer_input_values.append(
                    dict(base_answer_input_vals, question_id=question.id, value_text_box=partner_inputs[question.id].strip())
                )

        booking_line_values = []
        if appointment_type.schedule_based_on == 'resources':
            capacity_to_assign = asked_capacity
            for resource in resources:
                resource_remaining_capacity = resources_remaining_capacity.get(resource)
                new_capacity_reserved = min(resource_remaining_capacity, capacity_to_assign, resource.capacity)
                capacity_to_assign -= new_capacity_reserved
                booking_line_values.append({
                    'appointment_resource_id': resource.id,
                    'capacity_reserved': new_capacity_reserved,
                    'capacity_used': new_capacity_reserved if resource.shareable and appointment_type.capacity_type != 'single_booking' else resource.capacity,
                })
                print("booking_value", booking_line_values , "end", asked_capacity,"en", new_capacity_reserved)
        else:
            user_remaining_capacity = users_remaining_capacity['total_remaining_capacity']
            new_capacity_reserved = min(user_remaining_capacity, asked_capacity, appointment_type.user_capacity_count)
            booking_line_values.append({
                    'appointment_user_id': staff_user.id,
                    'capacity_reserved': new_capacity_reserved,
                    'capacity_used': new_capacity_reserved,
                })
        if invite_token:
            appointment_invite = request.env['appointment.invite'].sudo().search([('access_token', '=', invite_token)])
        else:
            appointment_invite = request.env['appointment.invite']

        return self._handle_appointment_form_submission(
            appointment_type, date_start, date_end, duration, answer_input_values, name,
            customer, appointment_invite, guests, staff_user, asked_capacity, booking_line_values
        )

    def _slot_availability_prepare_users_bookings_values(self, users, start_dt_utc, end_dt_utc):
        """ This method computes bookings of users between start_dt and end_dt
        of appointment check. Also, users are shared between multiple appointment
        type. So we must consider all bookings in order to avoid booking them more than once.

        :param <res.users> users: prepare values to check availability
          of those users against given appointment boundaries. At this point
          timezone should be correctly set in context of those users;
        :param datetime start_dt_utc: beginning of appointment check boundary. Timezoned to UTC;
        :param datetime end_dt_utc: end of appointment check boundary. Timezoned to UTC;

        :return: dict containing main values for computation, formatted like
          {
            'users_to_bookings': bookings, formatted as a dict
              {
                'appointment_user_id': recordset of booking line,
                ...
              },
          }
        """

        users_to_bookings = {}
        if users:
            booking_lines = self.env['appointment.booking.line'].sudo().search([
                ('appointment_user_id', 'in', users.ids),
                ('event_start', '<', end_dt_utc),
                ('event_stop', '>', start_dt_utc),
            ])

            users_to_bookings = booking_lines.grouped('appointment_user_id')
        return {
            'users_to_bookings': users_to_bookings,
        }
    
