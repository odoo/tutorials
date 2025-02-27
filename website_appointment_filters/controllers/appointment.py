# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class WebsiteAppointmentFiltersController(WebsiteAppointment):
    @http.route(['/appointment'], type='http', auth='public', website=True)
    def appointment_type_index(self, **filters):
        response = super().appointment_type_index()

        type_mapping = {
            'online': ('location_id', '=', None),
            'offline': ('location_id', '!=', None),
        }

        payment_step_mapping = {
            'paid': ('has_payment_step', '=', True),
            'free': ('has_payment_step', '=', False),
        }

        schedule_mapping = {
            'users': ('schedule_based_on', '=', 'users'),
            'resources': ('schedule_based_on', '=', 'resources'),
        }

        domain = []
        filters_active = []

        for filter_key, mapping in [
            ('type', type_mapping),
            ('payment_step', payment_step_mapping),
            ('schedule', schedule_mapping),
        ]:
            if filter_key in filters and filters[filter_key] in mapping:
                domain.append(mapping[filters[filter_key]])
                filters_active.append(f"{filter_key.capitalize()}: {filters[filter_key]}")

        appointment_types = request.env['appointment.type'].search(domain)
        print_active_filters = ', '.join(filters_active)
        response.qcontext['appointment_types'] = appointment_types
        response.qcontext['print_active_filters'] = print_active_filters
        return response
