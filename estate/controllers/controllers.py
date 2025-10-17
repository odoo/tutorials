from datetime import datetime
from odoo import http
from odoo.http import request


class EstateProperties(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"], website=True, auth="public"
    )
    def get_properties(self, page=1, **kwargs):
        page = int(page)
        properties_per_page = 6
        domain = [("state", "in", ["new", "offer received"])]

        listed_after = kwargs.get("listed_after")
        searching_name = kwargs.get("search")

        if listed_after:
            try:
                date_obj = datetime.strptime(listed_after, "%Y-%m-%d")
                domain.append(('create_date', '>', date_obj))
            except ValueError:
                pass  

        if searching_name:
            domain.append(('name', 'ilike', searching_name))

        total_properties = request.env["estate.property"].sudo().search_count(domain)
        pager = request.website.pager(
            url="/properties",
            page=page,
            total=total_properties,
            step=properties_per_page,
        )
        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, limit=properties_per_page, offset=pager['offset'])
        )
        return request.render(
            "estate.estate_property_listing_template",
            {
                "properties": properties,
                "pager": pager,
            },
        )

    @http.route("/property/<int:property_id>", type="http", auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env["estate.property"].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render("estate.property_detail_template", {"property": property})
