from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route("/properties", type="http", auth="public", website=True)
    def property_list(self, **kwargs):
        """Renders a list of all available properties"""
        print("-----------------------------")
        properties = request.env["estate.property"].sudo().search([])
        return request.render("estate.estate_property_list_template", {"properties": properties})
