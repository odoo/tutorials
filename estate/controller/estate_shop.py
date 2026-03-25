from odoo import http
from odoo.http import request


class EstateShop(http.Controller):
    @http.route(
        ["/shop2", "/shop2/page/<int:page>"], type="http", auth="public", website=True,
    )
    def show_properties(self, page=1, search="", **kwargs):
        Property = request.env["estate.property"].sudo()
        domain = []
        if search:
            domain += ["|", ("name", "ilike", search), ("description", "ilike", search)]
        ppg = 6
        total = Property.search_count(domain)
        pager = request.website.pager(
            url="/shop2",
            total=total,
            page=page,
            step=ppg,
            url_args={"search": search},
        )
        properties = Property.search(domain, limit=ppg, offset=pager["offset"])
        return request.render(
            "estate.property_list_page",
            {
                "properties": properties,
                "pager": pager,
                "search": search,
            },
        )
