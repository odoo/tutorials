import math
from datetime import datetime
from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    @http.route(
        ["/properties","/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def list_properties(self, listed_after=None, search=None, page=1, **kwargs):
        # print("POST data received:", request.params)
        properties_per_page = 6
        domain = [("state", "in", ("new", "offer_received"))]

        if search:
            domain.append(('name', 'ilike', search))

        if listed_after:
            try:
                listed_after_date = datetime.strptime(listed_after, "%Y-%m-%d").date()
                domain.append(("create_date", ">", listed_after_date))
            except ValueError:
                pass

        total_properties = request.env["estate.property"].sudo().search_count(domain)

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=properties_per_page,
            url_args={"listed_after": listed_after, "search": search},
        )
        properties = request.env["estate.property"].sudo().search(
            domain, limit=properties_per_page, offset=pager["offset"]
        )
        
        return request.render(
            "estate.property_list_template",
            {
                "properties": properties,
                "pager": pager, 
                'listed_after': listed_after or '',
                'search_query': search or ''
            },
        )

    @http.route("/property/<int:property_id>", type="http", auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env["estate.property"].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render("estate.property_detail_template", {"property": property})

