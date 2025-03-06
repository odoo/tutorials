from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):

    @http.route('/properties', type='http', auth="public", website=True)
    def properties_page(self, **kwargs):
        return request.render("estate.estate_property_template")
