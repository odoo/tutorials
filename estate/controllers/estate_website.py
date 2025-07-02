from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def list_properties(self, page=1, **kwargs):
        step = 6
        offset = (page - 1) * step
        listed_after = kwargs.get("listed_after", None)
        search_term = kwargs.get("search", "").strip()

        domain = [("status", "not in", ["sold", "archived"]), ("active", "=", True)]

        if listed_after:
            domain.append(("create_date", ">=", listed_after))
        if search_term:
            domain.append(("name", "ilike", search_term))

        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, limit=step, offset=offset, order="create_date desc")
        )
        total_properties = request.env["estate.property"].sudo().search_count(domain)
        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            step=step,
            page=page,
            url_args={"search": search_term, "listed_after": listed_after},
        )

        return request.render(
            "estate.listing_page",
            {
                "properties": properties,
                "pager": pager,
                "listed_after": listed_after,
                "search_term": search_term,
            },
        )

    @http.route(
        "/property/<model('estate.property'):property>",
        type="http",
        auth="public",
        website=True,
    )
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
