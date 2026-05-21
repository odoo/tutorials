from odoo import http
from odoo.http import request


class WebsiteEstateController(http.Controller):
    @http.route("/properties", type="http", auth="public", website=True)
    def properties(self, page=1):

        properties = request.env["estate.property"].search([])

        return request.render(
            "estate.estate_property_home_page", {"properties_test": properties}
        )
