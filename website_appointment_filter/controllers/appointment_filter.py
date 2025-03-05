# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request


class WebsiteAppointmentkwargsController(WebsiteAppointment):
    @http.route(['/appointment'], type='http', auth='public', website=True)
    def appointment_type_index(self, **kwargs):
        response = super().appointment_type_index()
        domain = []

        if kwargs.get('type') == 'online':
            domain.append(('location_id', '=', None))
        elif kwargs.get('type') == 'offline':
            domain.append(('location_id', '!=', None))

        if kwargs.get('payment_step') == 'paid':
            domain.append(('has_payment_step', '=', True))
        elif kwargs.get('payment_step') == 'free':
            domain.append(('has_payment_step', '=', False))

        if kwargs.get('schedule') == 'users':
            domain.append(('schedule_based_on', '=', 'users'))
        elif kwargs.get('schedule') == 'resources':
            domain.append(('schedule_based_on', '=', 'resources'))

        appointment_types = request.env['appointment.type'].sudo().search(domain)
        response.qcontext['appointment_types'] = appointment_types
        return response
