from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class WebsiteAppointmentFilter(WebsiteAppointment):

    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        filter_domain = []

        if kwargs.get("appointment_type"):
            if kwargs["appointment_type"] == "online":
                filter_domain.append(("location_id", "=", False))
            elif kwargs["appointment_type"] == "offline":
                filter_domain.append(("location_id", "!=", False))

        if kwargs.get("payment_step"):
            if kwargs["payment_step"] == "required":
                filter_domain.append(("has_payment_step", "=", True))
            elif kwargs["payment_step"] == "not_required":
                filter_domain.append(("has_payment_step", "=", False))

        if kwargs.get("schedule_based_on"):
            if kwargs["schedule_based_on"] == "users":
                filter_domain.append(("schedule_based_on", "=", "users"))
            elif kwargs["schedule_based_on"] == "resources":
                filter_domain.append(("schedule_based_on", "=", "resources"))

        domain = self._appointments_base_domain(
            filter_appointment_type_ids=kwargs.get('filter_appointment_type_ids'),
            search=kwargs.get('search'),
            additional_domain=filter_domain
        )

        available_appointment_types = self._fetch_and_check_private_appointment_types(
            kwargs.get('filter_appointment_type_ids'),
            kwargs.get('filter_staff_user_ids'),
            kwargs.get('filter_resource_ids'),
            kwargs.get('invite_token'),
            domain=domain
        )

        return request.render(
            'website_appointment.appointments_cards_layout',
            self._prepare_appointments_cards_data(
                page, available_appointment_types, **kwargs
            )
        )
