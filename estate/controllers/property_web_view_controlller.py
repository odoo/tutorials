from odoo import http
from odoo.http import request


class PropertyWebView(http.Controller):
    @http.route(["/properties"], type="http", auth="public")
    def show_properties(self):
        properties = request.env["estate.property"].search([
            ('state', 'not in', ['sold', 'cancelled']),
            ('active', '=', 'True')
        ])
        return request.render(
            "estate.estate_property_web_view", {"properties": properties}
        )
