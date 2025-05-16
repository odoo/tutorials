from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(["/property"], auth="public", type="http", website="True")
    def list_properties(self , status=''):
        # Filter the properties based on the selected status
        if status == "new":
            domain = [("status", "=", "new")]
        elif status == "offer_receive":
            domain = [("status", "=", "offer_receive")]
        elif status == "offer_accept":
            domain = [("status", "=", "offer_accept")]
        elif status == "":
            domain = [
                ("status", "not in", ["cancelled"]),
                ("active", "=", True),
            ]

        properties = request.env["estate.property"].search(domain)
        return request.render(
            "estate.property_listing_page",
            {"properties": properties, "status": status},
        )

    @http.route(
        "/property/<model('estate.property'):property>",
        type="http",
        auth="public",
        website="True",
    )
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
