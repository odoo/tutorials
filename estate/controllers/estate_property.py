from odoo import http
from odoo.http import request


class PropertyWebsite(http.Controller):

    @http.route('/properties', auth='public', website=True)
    def list_properties(self, **kwargs):
        properties = request.env["estate.property"].sudo().search([("state", "not in", ["sold", "canceled"])])

        return request.render('estate.property_list_template', {'properties': properties})

    @http.route('/property/<int:property_id>', auth='public', website=True)
    def property_details(self, property_id):
        property = request.env["estate.property"].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render('estate.property_details_template', {'property': property})
