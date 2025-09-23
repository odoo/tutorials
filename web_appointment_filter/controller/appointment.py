from odoo import http
from odoo.http import request
from odoo.addons.base.models.ir_qweb import keep_query
from odoo.addons.appointment.controllers.appointment import AppointmentController


class WebsiteFilterController(AppointmentController):
    @http.route()
    def appointment_type_index(self, page=1, **kwargs):
        """
        Display the appointments to choose (the display depends of a custom option called 'Card Design')

        :param page: the page number displayed when the appointments are organized by cards

        A param filter_appointment_type_ids can be passed to display a define selection of appointments types.
        This param is propagated through templates to allow people to go back with the initial appointment
        types filter selection
        """
        kwargs["domain"] = self._appointments_base_domain(
            filter_appointment_type_ids=kwargs.get(
                "filter_appointment_type_ids"),
            search=kwargs.get("search"),
            invite_token=kwargs.get("invite_token"),
            additional_domain=self._appointment_website_domain(),
            filter_countries=True,
        )

        selected_schedule = kwargs.get("schedule_based_on")
        if selected_schedule and "domain" in kwargs:
            kwargs["domain"] += [("schedule_based_on", "=", selected_schedule)]

        selected_location_type = kwargs.get("location_type")
        if selected_location_type and "domain" in kwargs:
            if selected_location_type == "Offline":
                kwargs["domain"] += [("location_id", "!=", False)]
            else:
                kwargs["domain"] += [("location_id", "=", False)]

        selected_payment_type = kwargs.get("payment_type")
        if selected_payment_type and "domain" in kwargs:
            if selected_payment_type == "With Payment":
                kwargs["domain"] += [("has_payment_step", "=", True)]
            else:
                kwargs["domain"] += [("has_payment_step", "=", False)]

        available_appointment_types = self._fetch_and_check_private_appointment_types(
            kwargs.get("filter_appointment_type_ids"),
            kwargs.get("filter_staff_user_ids"),
            kwargs.get("filter_resource_ids"),
            kwargs.get("invite_token"),
            domain=kwargs["domain"],
        )
        if len(available_appointment_types) == 1 and not kwargs.get("search"):
            # If there is only one appointment type available in the selection, skip the appointment type selection view
            return request.redirect(
                "/appointment/%s?%s" % (available_appointment_types.id,
                                        keep_query("*"))
            )

        cards_layout = request.website.viewref(
            "website_appointment.opt_appointments_list_cards"
        ).active

        AppointmentType = request.env["appointment.type"]
        availability_on_dict = dict(
            AppointmentType._fields["schedule_based_on"].selection
        )
        location_type = ["Online", "Offline"]
        payment_type = ["With Payment", "Without Payment"]
        values = {
            "availability_on_dict": availability_on_dict,
            "selected_schedule": selected_schedule,
            "location_type": location_type,
            "selected_location_type": selected_location_type,
            "payment_type": payment_type,
            "selected_payment_type": selected_payment_type,
        }

        if cards_layout:
            data = self._prepare_appointments_cards_data(
                page, available_appointment_types, **kwargs
            )
            data.update(values)
            return request.render(
                "website_appointment.appointments_cards_layout",
                data,
            )
        else:
            return request.render(
                "appointment.appointments_list_layout",
                self._prepare_appointments_list_data(
                    available_appointment_types, **kwargs
                ),
            )
