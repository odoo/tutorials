from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment


class WebsiteAppointmentFiltered(WebsiteAppointment):
    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        available_domain = self._appointment_website_domain()
        extra_domain = []

        if kwargs.get("appointment_mode") == "online":
            extra_domain.append(("location_id", "=", False))
        elif kwargs.get("appointment_mode") == "offline":
            extra_domain.append(("location_id", "!=", False))

        if kwargs.get("schedule_based_on") == "user":
            extra_domain.append(("schedule_based_on", "=", "users"))
        elif kwargs.get("schedule_based_on") == "resource":
            extra_domain.append(("schedule_based_on", "=", "resources"))

        if kwargs.get("has_payment_step") == "true":
            extra_domain.append(("has_payment_step", "=", True))
        elif kwargs.get("has_payment_step") == "false":
            extra_domain.append(("has_payment_step", "=", False))

        final_domain = available_domain + extra_domain
        response = super().appointment_type_index(page=page, **kwargs)

        appointment_types = response.qcontext.get("appointment_types", [])
        filtered_appointments = appointment_types.filtered_domain(final_domain)

        response.qcontext["appointment_types"] = filtered_appointments
        response.qcontext["filters"] = {
            "appointment_mode": kwargs.get("appointment_mode"),
            "schedule_based_on": kwargs.get("schedule_based_on"),
            "has_payment_step": kwargs.get("has_payment_step"),
        }
        return response
