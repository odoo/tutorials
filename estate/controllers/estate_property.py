from odoo import http
from odoo.http import request


class PropertyController(http.Controller):
    @http.route("/properties", type="http", auth="public", website=True)
    def properties_list(self, **kw):
        properties = request.env["estate.property"].search([])
        return request.render("estate.properties_page_view", {"properties": properties})
