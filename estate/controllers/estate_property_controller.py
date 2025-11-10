from odoo import http
from odoo.http import request
from datetime import datetime


class EstatePropertyController(http.Controller):

    @http.route(["/real_estate", '/real_estate/page/<int:page>'], type="http", auth="user", website=True)
    def properties_list(self, page=1, **kw):
        properties_per_page = 10
        EstateProperty = request.env["estate.property"].sudo()

        domain = []
        if not request.env.user.has_group("estate.estate_group_manager"):
            domain.append(("website_published", "=", True))

        listed_after = kw.get("listed_after")
        if listed_after:
            try:
                selected_date = datetime.strptime(listed_after, "%Y-%m-%d")
                domain.append(("create_date", ">", selected_date))
            except ValueError:
                pass         
        total_properties = EstateProperty.search_count(domain)

        offset = (page - 1) * properties_per_page
        properties = EstateProperty.search(domain, offset=offset, limit=properties_per_page)

        pager = request.website.pager(
            url="/real_estate",
            total=total_properties,
            page=page,
            step=properties_per_page
        )

        return request.render(
            "estate.property_listing_page",
            {
                "properties": properties,
                "pager": pager,
                "selected_date": listed_after or ""
            },
        )

    @http.route("/real_estate/<int:property_id>", type="http", auth="public", website=True)
    def property_detail(self, property_id):
        property_record = request.env["estate.property"].sudo().browse(property_id)

        if not property_record.exists():
            return request.render("website.404")

        return request.render("estate.property_detail_page", {"property": property_record})
