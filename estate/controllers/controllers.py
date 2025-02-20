from datetime import datetime
import math

from odoo import http
from odoo.http import request, route


class EstatePropertyController(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
    )
    def show_properties(self, page=1, listed_after=None, search=None, **post):
        domain = [("state", "in", ["new", "offer received"])]
        # current issue is that the list and search wont be stacked it will rather overwrite will add this feature soon.
        if search:
            domain.append(("name", "ilike", search))
            domain.insert(0,"&")
        if listed_after:
            try:
                date_filter = datetime.strptime(listed_after, "%Y-%m-%d")
                domain.insert(0,"&")
                domain.append(("create_date", ">", date_filter))
            except ValueError:
                pass
        if listed_after and search:
            domain.insert(0,"&")
            domain.insert(1,"&")
            domain.append(("create_date", ">", date_filter))
            domain.append(("name", "ilike", search))
        print(domain)
        total_properties = request.env["estate.property"].sudo().search_count(domain)

        total_pages = math.ceil(total_properties / 6)
        pager = request.website.pager(
            url="/properties",  # base URL
            total=total_properties,  # total item count
            page=page,  # current page
            step=6,  # items per page
            scope=total_pages,  # typically `self`
            url_args={'search':search,'listed_after':listed_after}if listed_after or search else{},  # additional GET params if needed
        )
        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, limit=6, offset=pager["offset"])
        )

  
        return request.render(
            "estate.estate_property_webpage",
            {
                "properties": properties,
                "total_pages": int(total_pages),
                "current_page": int(page),
                "pager": pager,
            },
        )

    @http.route(
        "/properties/details/<model('estate.property'):property>",
        type="http",
        auth="public",
        website=True,
    )
    def property_details(self, property, **kw):
        return request.render("estate.estate_property_details", {"property": property})
