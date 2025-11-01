# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons.website_appointment.controllers.appointment import WebsiteAppointment
from odoo.http import request

class WebsiteAppointmentFiltersController(WebsiteAppointment):
    @http.route(['/appointment'], type='http', auth='public', website=True)
    def appointment_type_index(self, **kwargs):
        response = super().appointment_type_index()
        
        # Get all initial appointment types from the parent method
        all_appointment_types = response.qcontext.get('appointment_types', request.env['appointment.type'].sudo())
        
        # Extract filter parameters
        filter_type = kwargs.get('type')
        filter_payment = kwargs.get('payment_step')
        filter_schedule = kwargs.get('schedule')
        
        # Start with the base domain - maintaining compatibility with parent controller
        domain = [('website_published', '=', True)]
        filter_descriptions = []
        
        # Apply type filter (online/offline)
        if filter_type == 'online':
            domain.append(('location_id', '=', False))
            filter_descriptions.append(_("Online appointments"))
        elif filter_type == 'offline':
            domain.append(('location_id', '!=', False))
            filter_descriptions.append(_("Offline appointments"))
            
        # Apply payment filter
        if filter_payment == 'paid':
            domain.append(('has_payment_step', '=', True))
            filter_descriptions.append(_("Paid appointments"))
        elif filter_payment == 'free':
            domain.append(('has_payment_step', '=', False))
            filter_descriptions.append(_("Free appointments"))
            
        # Apply schedule filter
        if filter_schedule == 'users':
            domain.append(('schedule_based_on', '=', 'users'))
            filter_descriptions.append(_("User-based scheduling"))
        elif filter_schedule == 'resources':
            domain.append(('schedule_based_on', '=', 'resources'))
            filter_descriptions.append(_("Resource-based scheduling"))
        
        # Get filtered appointment types if any filters are applied
        total_count = len(all_appointment_types)
        filtered_count = None
        if len(domain) > 1:  # More than just the website_published filter
            filtered_types = request.env['appointment.type'].sudo().search(domain)
            response.qcontext['appointment_types'] = filtered_types
            filtered_count = len(filtered_types)
        
        # Add filter information to context
        has_filters = bool(filter_type and filter_type != 'all' or 
                          filter_payment and filter_payment != 'all' or 
                          filter_schedule and filter_schedule != 'all')
        
        # Format the active filters text for display
        active_filters_text = []
        if filter_descriptions:
            active_filters_text.extend(filter_descriptions)        
        print("active_filters_text", active_filters_text)
        
        response.qcontext.update({
            'active_filters': filter_descriptions,
            'current_filters': {
                'type': filter_type,
                'payment_step': filter_payment, 
                'schedule': filter_schedule
            },
            'has_filters': has_filters,
            'filtered_count': filtered_count,
            'total_count': total_count,
            'print_active_filters': active_filters_text,
        })
        
        return response
