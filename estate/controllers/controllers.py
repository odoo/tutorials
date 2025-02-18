from odoo import http
from odoo.http import request, route


class EstatePropertyController(http.Controller):
    @http.route(
        ["/properties"],
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
    )
    def show_properties(self, page=1,**post):
        properties = (
            request.env["estate.property"]
            .sudo()
            .search([("state", "in", ["new", "offer received"])],limit=6,offset=(int(page)-1)*6)
        )
        total_properties = (
            request.env["estate.property"]
            .sudo()
            .search_count([("state", "in", ["new", "offer received"])])
        )
        total_pages = total_properties / 6
        return request.render(
            "estate.estate_property_webpage",
            {
                "properties": properties,
                "total_pages": total_pages,
                "current_page": page,
            },
        )

    @http.route("/properties/details", type="http", auth="public", website=True)
    def property_details(self, id=None, **kw):
        pass
