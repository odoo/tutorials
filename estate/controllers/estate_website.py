from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def list_properties(self, page=1, **kwargs):
        # Fetch all estate properties from the database
        properties = request.env["estate.property"].sudo().search([])
        total_properties = len(properties)
        print(total_properties)
        website = request.env['website'].get_current_website()

        pager = website.pager(
            url="/properties",
            total=total_properties,
            step=6,
        )
        return request.render(
            "estate.listing_page", {"properties": properties, "pager": pager}
        )
