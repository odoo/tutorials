from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(
        ["/property"],
        auth="public",
        type="http",
    )
    def list_properties(self):
        properties = request.env["estate.property"].search([])
        return request.render(
            "estate.property_listing_page",
            {"properties": properties},
        )

    @http.route(
        "/property/<model('estate.property'):property>",
        type="http",
        auth="public",
    )
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
