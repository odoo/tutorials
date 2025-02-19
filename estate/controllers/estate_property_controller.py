from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def estate_property(self, page=1, **kw):
        offset = (int(page) - 1) * 6

        listed_after = kw.get("listed_after", False)
        search = kw.get('search',False)

        domain = [("state", "in", ["new", "offer_received"])]
        if listed_after:
            domain.append(("date_availability", ">", listed_after))

        if search:
            domain.append(("name", "ilike", search))  

        properties = request.env["estate.property"].search(
            domain, limit=6, offset=offset, order="create_date desc"
        )
        total_properties = request.env["estate.property"].search_count(domain)

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=int(page),
            step=6,
            url_args=kw,
        )

        return request.render(
            "estate.properties_page",
            {"properties": properties, "pager": pager, "listed_after": listed_after, "search": search},
        )

    @http.route(
        ['/property/<model("estate.property"):property>'],
        type="http",
        auth="public",
        website=True,
    )
    def property_detail(self, property, **kw):
        return request.render(
            "estate.property_detail",
            {"property": property},
        )
