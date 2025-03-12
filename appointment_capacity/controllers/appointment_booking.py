import json
import pytz 
import re
from dateutil.relativedelta import relativedelta
from urllib.parse import unquote_plus
from werkzeug.exceptions import NotFound
from odoo import fields
from odoo.http import request
from odoo import http
from odoo.addons.base.models.ir_qweb import keep_query
from odoo.addons.phone_validation.tools import phone_validation
from odoo.addons.appointment.controllers.appointment import AppointmentController

class AppointmentCapacityOverride(AppointmentController):

    def _prepare_appointment_type_page_values(self, appointment_type, staff_user_id=False, resource_selected_id=False, **kwargs):
        res = super()._prepare_appointment_type_page_values(appointment_type, staff_user_id, resource_selected_id, **kwargs)

        filter_resource_ids = json.loads(kwargs.get('filter_resource_ids') or '[]')
        resources_possible = self._get_possible_resources(appointment_type, filter_resource_ids)
        resource_default = resource_selected = request.env['appointment.resource']
        staff_user_id = int(staff_user_id) if staff_user_id else False
        resource_selected_id = int(resource_selected_id) if resource_selected_id else False
        manage_capacity_type = appointment_type.resource_capacity

        max_capacity_possible = 0

        if resources_possible:
            if resource_selected_id and resource_selected_id in resources_possible.ids and appointment_type.assign_method != 'time_resource':
                resource_selected = request.env['appointment.resource'].sudo().browse(resource_selected_id)
            elif appointment_type.assign_method == 'resource_time':
                resource_default = resources_possible[0]

        # my code changes
        manage_capacity_type = appointment_type.resource_capacity
        if manage_capacity_type == 'one_booking' or manage_capacity_type == 'multi_booking':
            max_capacity_possible = 1
        elif manage_capacity_type == 'multi_seat':
            if appointment_type.schedule_based_on == 'users':
                max_capacity_possible = appointment_type.capacity_count or 1  # Default to 1 if not set
            else:
                possible_combinations = (resource_selected or resource_default or resources_possible)._get_filtered_possible_capacity_combinations(1, {})
                max_capacity_possible = possible_combinations[-1][1] if possible_combinations else 1
        res['max_capacity'] = min(12, max_capacity_possible)
        return res

    @http.route(['/appointment/<int:appointment_type_id>/submit'],
                type='http', auth="public", website=True, methods=["POST"])
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
            # change for the users selection
        else:
            # check availability of the selected user again (in case someone else booked while the client was entering the form)
            staff_user = request.env['res.users'].sudo().search([('id', '=', int(staff_user_id))])
            if staff_user not in appointment_type.staff_user_ids:
                raise NotFound()
            users_remaining_capacity = appointment_type._get_users_remaining_capacity(staff_user, date_start, date_end)
            if staff_user and not staff_user.partner_id.calendar_verify_availability(date_start, date_end) or (appointment_type.resource_capacity != 'one_booking' and users_remaining_capacity['total_remaining_capacity'] < asked_capacity):
                return request.redirect('/appointment/%s?%s' % (appointment_type.id, keep_query('*', state='failed-staff-user')))

        guests = None
        if appointment_type.allow_guests:
            if guest_emails_str:
                guests = request.env['calendar.event'].sudo()._find_or_create_partners(guest_emails_str)

        customer = self._get_customer_partner()

        # email is mandatory
        new_customer = not customer.email
        if not new_customer and customer.email != email and customer.email_normalized != email_normalize(email):
            new_customer = True
        if not new_customer:
            # phone is mandatory
            if not customer.phone:
                customer.phone = customer._phone_format(number=phone) or phone
            else:
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
        resource_capacity = appointment_type.resource_capacity
        if appointment_type.schedule_based_on == 'resources':
            capacity_to_assign = asked_capacity
            for resource in resources:
                resource_remaining_capacity = resources_remaining_capacity.get(resource)
                new_capacity_reserved = min(resource_remaining_capacity, capacity_to_assign, resource.capacity)
                capacity_to_assign -= new_capacity_reserved
                booking_line_values.append({
                    'appointment_resource_id': resource.id,
                    'capacity_reserved': new_capacity_reserved,
                    'capacity_used': new_capacity_reserved if resource_capacity != 'one_booking' and resource.shareable else resource.capacity
                })
                # changes for the users selection
        else:
            user_remaining_capacity = users_remaining_capacity['total_remaining_capacity']
            new_capacity_reserved = min(user_remaining_capacity, asked_capacity, appointment_type.capacity_count)
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
