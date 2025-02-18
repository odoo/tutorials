from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):
    @http.route(["/properties","/properties/page/<int:page>"], auth="user", website=True)
    def property_list(self, page=1, **kwargs):
        # Fetch all active, available properties
        domain = [("state", "in", ["new", "offer_received"]), ("active", "=", True)]
        properties = request.env["estate.property"].sudo().search(domain, limit=9, offset=(page-1)*9)
        # Total count for pagination
        total_properties = request.env["estate.property"].sudo().search_count(domain)
        # Prepare the pagination
        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=9
        )
        return request.render("estate.property_listing", {
            "properties": properties,
            "pager": pager,
        })

    @http.route("/property/<model('estate.property'):property_id>", auth="user", website=True)
    def property_details(self, property_id, **kwargs):
        return request.render("estate.property_detail", {
            "property": property_id,
        })
