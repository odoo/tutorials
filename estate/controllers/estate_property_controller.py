from datetime import datetime
from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def list_properties(self, page=1, **kwargs):
        # print("POST data received:", request.params)
        properties_per_page = 6
        offset = (page - 1) * properties_per_page
        domain = [("state", "in", ("new", "offer_received"))]
        listed_after = request.httprequest.form.get("listed_after")
        if listed_after:
            try:
                listed_after_date = datetime.strptime(listed_after, "%Y-%m-%d").date()
                domain.append(("create_date", ">", listed_after_date))
            except ValueError:
                pass
        total_properties = request.env["estate.property"].sudo().search_count(domain)
        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, limit=properties_per_page, offset=offset)
        )
        total_pages = total_properties / properties_per_page
        return request.render(
            "estate.property_list_template",
            {
                "properties": properties,
                "page": page,
                "total_pages": total_pages,
                "listed_after": listed_after,
            },
        )

    @http.route("/property/<int:property_id>", type="http", auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env["estate.property"].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render("estate.property_detail_template", {"property": property})

