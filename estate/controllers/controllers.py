from odoo import http
from odoo.http import request

class PropertyController(http.Controller):
    @http.route("/properties", auth="public", website=True)
    def list_properties(self, **kw):
        domain = [("state", "in", ["new", "offer_received", "offer_accepted"])]
        properties = request.env["estate.property"].search(domain)

        return request.render("estate.property_listing", {"properties": properties})
