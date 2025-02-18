from odoo import http
from odoo.http import route,request


class estate_property(http.Controller):
    @route('/estate/property', auth="user", type="http", website=True)
    def show_estate_propeties(self):
        properties = request.env['estate.property'].search([])
        return request.render("estate.estate_properties",{'properties':properties})
