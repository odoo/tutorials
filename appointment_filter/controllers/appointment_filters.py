from odoo import http
from odoo.http import request
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment


class WebsiteAppointmentFiltered(WebsiteAppointment):

    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        available_domain = self._appointment_website_domain()
        extra_domain = []

        filters = [
            {
                "label": "appointment_type",
                "value": "online",
                "condition": ("location_id", "=", False)
            },
            {
                "label": "appointment_type",
                "value": "offline",
                "condition": ("location_id", "!=", False)
            },
            {
                "label": "payment_step",
                "value": "required",
                "condition": ("has_payment_step", "=", True)
            },
            {
                "label": "payment_step",
                "value": "not_required",
                "condition": ("has_payment_step", "=", False)
            },
            {
                "label": "schedule_based_on",
                "value": "users",
                "condition": ("schedule_based_on", "=", "users")
            },
            {
                "label": "schedule_based_on",
                "value": "resources",
                "condition": ("schedule_based_on", "=", "resources")
            },
        ]
        for filter in filters:
            if kwargs.get(filter["label"]) == filter["value"]:
                extra_domain.append(filter["condition"])

        if kwargs.get("search"):
            extra_domain.append(("name", "ilike", kwargs["search"]))

        final_domain = available_domain + extra_domain
        appointments = request.env["appointment.type"].sudo().search(final_domain)

        values = self._prepare_appointments_cards_data(
            appointment_types=appointments,
            page=page,
            **kwargs  
        )

        return request.render("website_appointment.appointments_cards_layout", values)
