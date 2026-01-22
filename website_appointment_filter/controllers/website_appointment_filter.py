# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment  # type: ignore
from odoo.http import request

class WebsiteAppointmentFilter(WebsiteAppointment):

    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        available_domains = self._appointment_website_domain()
        filter_domain = []

        filters = {
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

        # Apply filters dynamically
        for key, mapping in filters.items():
            filter_value = kwargs.get(key)
            if filter_value and filter_value in mapping:
                filter_domain.append(mapping[filter_value])

        # Apply search filter
        if kwargs.get("search"):
            filter_domain.append(("name", "ilike", kwargs["search"]))

        # Perform search
        appointments = request.env["appointment.type"].sudo().search(available_domains + filter_domain)

        # Prepare and render the view
        values = self._prepare_appointments_cards_data(
            appointment_types=appointments, page=page, **kwargs
        )
        return request.render("website_appointment.appointments_cards_layout", values)
