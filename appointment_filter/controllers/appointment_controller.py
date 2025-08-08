from odoo import http
from odoo.http import request
from odoo.addons.appointment.controllers.appointment import AppointmentController


class CustomWebsiteAppointment(AppointmentController):

    @http.route(['/appointment', '/appointment/page/<int:page>'], type='http', auth="public", website=True, sitemap=True)
    def appointment_type_index(self, page=1, **searches):
        """Display appointments with filters for location, schedule-based type, and payment requirement."""
        if (
            searches.get('tags', '[]').count(',') > 0
            and request.httprequest.method == 'GET'
            and not searches.get('prevent_redirect')
        ):
            return request.redirect('/appointment', code=301)

        AppointmentType = request.env['appointment.type'].sudo()
        step = int(request.env['ir.config_parameter'].sudo().get_param('appointment_filter.step_value', 12))

        domain = self._appointments_base_domain(searches.get('filter_appointment_type_ids'))

        appointments = AppointmentType.with_context(prefetch_fields=False).search(domain)
        appointments_count = len(appointments)

        # Apply pagination manually
        appointments = appointments[(page - 1) * step : page * step]

        # Pagination setup
        pager = request.website.pager(
            url="/appointment",
            url_args=searches,
            total=appointments_count,
            page=page,
            step=step,
            scope=5
        )

        values = {
            'filter_appointment_type_ids': searches.get('filter_appointment_type_ids'),
            'appointment_types': appointments,
            'pager': pager,
            'searches': searches,
        }

        return request.render("appointment.appointments_list_layout", values)

    @classmethod
    def _appointments_base_domain(cls, filter_appointment_type_ids, search=False, invite_token=False, additional_domain=None):
        """Extends the base domain to include additional filters."""
        domain = super()._appointments_base_domain(filter_appointment_type_ids, search, invite_token, additional_domain)

        # Retrieve filters from request parameters safely
        filter_location = request.params.get('filter_location', '').strip().lower()
        if filter_location == 'online':
            domain.append(('location_id', '=', False))
        elif filter_location == 'offline':
            domain.append(('location_id', '!=', False))

        filter_based_on = request.params.get('filter_based_on', '').strip().lower()
        if filter_based_on == 'resource':
            domain.append(('schedule_based_on', '=', 'resources'))
        elif filter_based_on == 'user':
            domain.append(('schedule_based_on', '=', 'users'))

        filter_payment = request.params.get('filter_payment', '').strip().lower()
        if filter_payment == 'true':  
            domain.append(('has_payment_step', '=', True))
        elif filter_payment == 'false':  
            domain.append(('has_payment_step', '=', False))

        return domain
