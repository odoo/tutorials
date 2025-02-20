from datetime import datetime
from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route("/properties", type="http", auth="user", website=True)
    def list_properties(self, page=1, listed_after=None, **kwargs):
        """
        Fetch and display estate properties with pagination and filtering.

        - Filters properties based on user role:
        * Managers see all properties.
        * Regular users see only published properties.
        - Supports pagination (10 properties per page).
        - Optionally filters properties listed after a selected date.
        """
        per_page = 10
        offset = (page - 1) * per_page

        domain = [("state", "in", ["new", "offer_received", "offer_accepted"])]

        # Restrict visibility for non-managers
        if not request.env.user.has_group("estate.estate_group_manager"):
            domain.append(("is_published", "=", True))

        if listed_after:
            try:
                filter_date = datetime.strptime(listed_after, "%Y-%m-%d")
                domain.append(("create_date", ">", filter_date))
            except ValueError:
                pass

        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, offset=offset, limit=per_page, order="create_date desc")
        )

        total_properties = request.env["estate.property"].sudo().search_count(domain)

        pager = request.website.pager(
            url="/properties", total=total_properties, step=per_page, page=page
        )

        return request.render(
            "estate.property_listing_page",
            {
                "properties": properties,
                "pager": pager,
                "selected_date": listed_after or "",
            },
        )

    @http.route(
        ["/properties/<model('estate.property'):property>"],
        type="http",
        auth="user",
        website=True,
    )
    def show_property_details(self, property, **kwargs):
        return request.render(
            "estate.property_detail_page_template", {"property": property}
        )
