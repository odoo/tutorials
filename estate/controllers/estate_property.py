from odoo import http
from odoo.http import request


class property(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        website=True,
        auth="public",
    )
    def list_properties(self, page=1, **kwargs):
        per_page = 6

        Property = request.env["estate.property"].sudo()

        total_properties = Property.search_count(
            [("state", "in", ["new", "offer_received", "offer_accepted"])]
        )

        pager = request.website.pager(
            url="/properties", total=total_properties, page=page, step=per_page
        )

        properties = Property.search(
            [("state", "in", ["new", "offer_received", "offer_accepted"])],
            limit=per_page,
            offset=pager["offset"],
        )

        return request.render(
            "estate.property_list", {"properties": properties, "pager": pager}
        )

    @http.route("/property/<int:property_id>", type="http", website=True, auth="public")
    def property_details(self, property_id, **kwargs):
        Property = request.env["estate.property"].sudo().browse(property_id)
        if not Property:
            return request.not_found()
        salesperson = Property.salesperson_id
        return request.render(
            "estate.property_detail",
            {
                "property": Property,
                "salesperson": salesperson,
            },
        )
