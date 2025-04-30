from odoo import http
from odoo.http import request


class WebsiteAppointment(http.Controller):

    @http.route('/appointments', type='http', auth="public", website=True)
    def website_appointments(self, **kwargs):
        domain = []
