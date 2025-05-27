from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment


class WebsiteAppointmentFilter(WebsiteAppointment):
    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        return super().appointment_type_index(page, **kwargs)

    def _prepare_appointments_list_data(self, appointment_types=None, **kwargs):
        appointment_types = self._filter_appointment_types(appointment_types, **kwargs)
        has_payment_field = 'has_payment_step' in appointment_types.fields_get().keys()
        res = super()._prepare_appointments_list_data(appointment_types, **kwargs)
        return {**res, 'has_payment_field': has_payment_field}

    def _prepare_appointments_cards_data(self, page, appointment_types, **kwargs):
        appointment_types = self._filter_appointment_types(appointment_types, **kwargs)
        has_payment_field = 'has_payment_step' in appointment_types.fields_get().keys()
        res = super()._prepare_appointments_cards_data(page, appointment_types, **kwargs)
        return {**res, 'has_payment_field': has_payment_field}

    def _filter_appointment_types(self, appointment_types, **kwargs):
        if 'type' in kwargs:
            if kwargs.get('type') == 'online':
                appointment_types = appointment_types.filtered(lambda app: not app.location_id)
            elif kwargs.get('type') == 'offline':
                appointment_types = appointment_types.filtered(lambda app: app.location_id)
        if 'schedule' in kwargs:
            if kwargs.get('schedule') == 'user':
                appointment_types = appointment_types.filtered(lambda app: app.schedule_based_on=='users')
            elif kwargs.get('schedule') == 'resource':
                appointment_types = appointment_types.filtered(lambda app: app.schedule_based_on=='resources')
        if 'payment' in kwargs:
            if kwargs.get('payment') == 'yes':
                appointment_types = appointment_types.filtered(lambda app: app.has_payment_step)
            elif kwargs.get('payment') == 'no':
                appointment_types = appointment_types.filtered(lambda app: not app.has_payment_step)
        return appointment_types
