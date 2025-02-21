from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class EstatePropertyController(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"], auth="public", website=True
    )
    def my_site(self, page=1, **kwargs):
        listed_after = kwargs.get("listed_after")
        searching_name = kwargs.get("property_name")
        page = int(page)
        domain = [("status", "in", ["new", "offer_received"])]

        if listed_after:
            try:
                listed_after_date = datetime.strptime(listed_after, "%Y-%m-%d").date()
                domain.append(("date_availability", ">", listed_after_date))
            except ValueError:
                listed_after_date = None

        if searching_name:
            search_filter = [
                "|",
                ("name", "ilike", searching_name),
                ("description", "ilike", searching_name),
            ]
            domain.extend(search_filter)

        total_properties = request.env["estate.property"].sudo().search_count(domain)

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=6,
            url_args=kwargs,
        )

        properties = (
            request.env["estate.property"]
            .sudo()
            .search(
                domain, order="date_availability desc", limit=6, offset=pager["offset"]
            )
        )

        return request.render(
            "estate.property_page",
            {
                "properties": properties,
                "pager": pager,
            },
        )

    @http.route("/properties/<int:property_id>", auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env["estate.property"].sudo().browse(property_id)

        if not property.exists():
            return request.not_found()

        return request.render("estate.property_detail_page", {"property": property})
