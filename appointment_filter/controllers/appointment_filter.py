from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class AppointmentFilterController(WebsiteAppointment):
    def _appointments_base_domain(
        cls,
        filter_appointment_type_ids,
        search=False,
        invite_token=False,
        additional_domain=None,
    ):
        domain = super()._appointments_base_domain(
            filter_appointment_type_ids, search, invite_token, additional_domain
        )

        filter_location = request.params.get("filter_location")
        if filter_location == "Online":
            domain.append(("location_id", "=", False))
        elif filter_location == "Offline":
            domain.append(("location_id", "!=", False))

        filter_based_on = request.params.get("filter_based_on")
        if filter_based_on == "Users":
            domain.append(("schedule_based_on", "=", "users"))
        elif filter_based_on == "Resources":
            domain.append(("schedule_based_on", "=", "resources"))

        filter_payment = request.params.get("filter_payment")
        if filter_payment == "Required":
            domain.append(("has_payment_step", "=", True))
        elif filter_payment == "No Required":
            domain.append(("has_payment_step", "=", False))

        return domain

    def _prepare_appointments_cards_data(self, page, appointment_types, **kwargs):
        context = super()._prepare_appointments_cards_data(
            page, appointment_types, **kwargs
        )

        context["filters"] = {
            "filter_location": kwargs.get("filter_location"),
            "filter_based_on": kwargs.get("filter_based_on"),
            "filter_payment": kwargs.get("filter_payment"),
        }

        return context
