from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment  # type: ignore
from odoo.http import request


class WebsiteAppointmentFilter(WebsiteAppointment):
    @http.route()
    def appointment_type_index(self, page=1, **params):
        base_domain = self._appointment_website_domain()
        domain_type = self._build_filter_domain(params)
        total_domain = base_domain + domain_type

        available_appointments = (
            request.env["appointment.type"].sudo().search(total_domain)
        )
        appointment_data = self._prepare_appointments_cards_data(
            page, available_appointments, **params
        )

        cards_layout = request.website.viewref(
            "website_appointment.opt_appointments_list_cards"
        ).active

        if cards_layout:
            return request.render(
                "website_appointment.appointments_cards_layout",
                self._prepare_appointments_cards_data(
                    page, available_appointments, **params
                ),
            )
        else:
            return request.render(
                "appointment.appointments_list_layout",
                self._prepare_appointments_list_data(available_appointments, **params),
            )

        return request.render(
            "website_appointment.appointments_cards_layout", appointment_data
        )

    def _build_filter_domain(self, params):
        domain_type = []
        type_dict = {
            "appointment_type": {
                "online": ("location_id", "=", False),
                "offline": ("location_id", "!=", False),
            },
            "payment_step": {
                "required": ("has_payment_step", "=", True),
                "not_required": ("has_payment_step", "=", False),
            },
            "schedule_based_on": {
                "users": ("schedule_based_on", "=", "users"),
                "resources": ("schedule_based_on", "=", "resources"),
            },
        }

        for key, values in type_dict.items():
            value = params.get(key)
            if value and value in values:
                domain_type.append(values[value])

        if params.get("search"):
            domain_type.append(("name", "ilike", params["search"]))
        return domain_type
