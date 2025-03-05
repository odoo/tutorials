from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class WebsiteAppointmentFiltered(WebsiteAppointment):
    @classmethod
    def _appointments_base_domain(cls,filter_appointment_type_ids,search=False, invite_token=False,additional_domain=None):
        domain = super()._appointments_base_domain(filter_appointment_type_ids, search, invite_token, additional_domain)

        appointment_mode = request.params.get("appointment_mode")
        schedule_based_on = request.params.get("schedule_based_on")
        has_payment_step = request.params.get("has_payment_step")

        extra_domain = []

        if appointment_mode == "online":
            extra_domain.append(("location_id", "=", False))
        elif appointment_mode == "offline":
            extra_domain.append(("location_id", "!=", False))

        if schedule_based_on == "user":
            extra_domain.append(("schedule_based_on", "=", "users"))
        elif schedule_based_on == "resource":
            extra_domain.append(("schedule_based_on", "=", "resources"))

        if has_payment_step == "true":
            extra_domain.append(("has_payment_step", "=", True))
        elif has_payment_step == "false":
            extra_domain.append(("has_payment_step", "=", False))

        return domain + extra_domain

    def _prepare_appointments_cards_data(self, page, appointment_types, **kwargs):
        data = super()._prepare_appointments_cards_data(page, appointment_types, **kwargs)

        data["filters"] = {
            "appointment_mode": kwargs.get("appointment_mode", ""),
            "schedule_based_on": kwargs.get("schedule_based_on", ""),
            "has_payment_step": kwargs.get("has_payment_step", ""),
        }

        return data
