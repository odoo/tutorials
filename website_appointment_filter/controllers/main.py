from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class WebsiteAppointmentFiltersController(WebsiteAppointment):
    @http.route(["/appointment"], type="http", auth="public", website=True)
    def appointment_type_index(self, **filters):
        domain = []
        filters_active=[]

        if "mode" in filters:
            if filters["mode"] == "online":
                domain.append(("location_id", "=", None))
            elif filters["mode"] == "offline":
                domain.append(("location_id", "!=", None))

        if "type" in filters:
            if filters["type"] == "paid":
                domain.append(("has_payment_step", "=", True))
            elif filters["type"] == "free":
                domain.append(("has_payment_step", "=", False))

        if "schedule" in filters:
            if filters["schedule"] == "users":
                domain.append(("schedule_based_on", "=", "users"))
            elif filters["schedule"] == "resources":
                domain.append(("schedule_based_on", "=", "resources"))
        
        appointment_types = request.env["appointment.type"].search(domain)

        if "mode" in filters:
            filters_active.append(f"Mode: {filters['mode']}")
        if "type" in filters:
            filters_active.append(f"Type: {filters['type']}")
        if "schedule" in filters:
            filters_active.append(f"Schedule: {filters['schedule']}")

        print_active_filters=', '.join(filters_active)
        response = super().appointment_type_index()
        response.qcontext["appointment_types"] = appointment_types
        response.qcontext["print_active_filters"]=print_active_filters
        return response
