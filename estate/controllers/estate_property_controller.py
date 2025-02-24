from odoo import http
from odoo.http import request
from datetime import datetime

class EstatePropertyController(http.Controller):
    @http.route(["/properties","/properties/page/<int:page>"], auth="user", website=True)
    def property_list(self, listed_after=None, page=1, **kwargs):
        # Fetch all active, available properties
        domain = [("state", "in", ["new", "offer_received"]), ("active", "=", True)]
        if listed_after:
            try:
                listed_date = datetime.strptime(listed_after, '%Y-%m-%d')
                domain.append(('date_availability', '>=', listed_date))
            except ValueError:
                pass 
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
