from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class WebsiteAppointmentFilter(WebsiteAppointment):

    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        available_domains = self._appointment_website_domain()
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

        if kwargs.get("search"):
            filter_domain.append(("name", "ilike", kwargs["search"]))

        final_domains = available_domains + filter_domain
        appointments = request.env["appointment.type"].sudo().search(final_domains)

        values = self._prepare_appointments_cards_data(
            appointment_types=appointments, page=page, **kwargs
        )

        return request.render("website_appointment.appointments_cards_layout", values)
