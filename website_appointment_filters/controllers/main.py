from odoo import http
from odoo.http import request
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment

class WebsiteAppointmentFiltersController(WebsiteAppointment):
    @http.route(['/appointment'], type='http', auth='public', website=True)
    def appointment_type_index(self, page=1, **filters):
        filtered_appointments_by_mode = set()
        filtered_appointments_by_type = set()
        filtered_appointments_by_schedule = set()

        if 'mode' in filters:
            if filters['mode'] == 'online':
                for appointment in request.env['appointment.type'].search([('location_id', '=', None)]):
                    filtered_appointments_by_mode.add(appointment.id)
            elif filters['mode'] == 'offline':
                for appointment in request.env['appointment.type'].search([('location_id', '!=', None)]):
                    filtered_appointments_by_mode.add(appointment.id)
            elif filters['mode'] == 'all':
                for appointment in request.env['appointment.type'].search([]):
                    filtered_appointments_by_mode.add(appointment.id)
        else:
            for appointment in request.env['appointment.type'].search([]):
                filtered_appointments_by_mode.add(appointment.id)

        if 'type' in filters:
            if filters['type'] == 'paid':
                for appointment in request.env['appointment.type'].search([('has_payment_step', '=', 'true')]):
                    filtered_appointments_by_type.add(appointment.id)
            elif filters['type'] == 'free':
                for appointment in request.env['appointment.type'].search([('has_payment_step', '!=', 'null')]):
                    filtered_appointments_by_type.add(appointment.id)
            elif filters['type'] == 'all':
                for appointment in request.env['appointment.type'].search([]):
                    filtered_appointments_by_type.add(appointment.id)
        else:
            for appointment in request.env['appointment.type'].search([]):
                filtered_appointments_by_type.add(appointment.id)

        if 'schedule' in filters:
            if filters['schedule'] == 'resources':
                for appointment in request.env['appointment.type'].search([('schedule_based_on', '=', 'resources')]):
                    filtered_appointments_by_schedule.add(appointment.id)
            elif filters['schedule'] == 'users':
                for appointment in request.env['appointment.type'].search([('schedule_based_on', '=', 'users')]):
                    filtered_appointments_by_schedule.add(appointment.id)
            elif filters['schedule'] == 'all':
                for appointment in request.env['appointment.type'].search([]):
                    filtered_appointments_by_schedule.add(appointment.id)
        else:
            for appointment in request.env['appointment.type'].search([]):
                filtered_appointments_by_schedule.add(appointment.id)

        filtered_appointments_by_mode = set(map(lambda id: str(id), filtered_appointments_by_mode))
        filtered_appointments_by_type = set(map(lambda id: str(id), filtered_appointments_by_type))
        filtered_appointments_by_schedule = set(map(lambda id: str(id), filtered_appointments_by_schedule))

        filters['filter_appointment_type_ids'] = f"[{','.join(filtered_appointments_by_mode & filtered_appointments_by_type & filtered_appointments_by_schedule)}]"

        if 'mode' not in filters.keys():
            filters['mode'] = 'all'
        if 'type' not in filters.keys():
            filters['type'] = 'all'
        if 'schedule' not in filters.keys():
            filters['schedule'] = 'all'
        

        return super().appointment_type_index(**filters)

    def _prepare_appointments_cards_data(self, page, appointment_types, **kwargs):
        res = super()._prepare_appointments_cards_data(page, appointment_types, **kwargs)
        res.update(kwargs)
        return res
