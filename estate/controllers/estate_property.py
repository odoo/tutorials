from odoo import http
from odoo.http import route, request


class EstateProperty(http.Controller):
    @route(
        ["/estate/property", "/estate/property/<int:property_id>"],
        auth="user",
        type="http",
        website=True,
    )
    def show_estate_properties(self, property_id=None):
        per_page = 3
        if property_id:
            property = request.env["estate.property"].browse(property_id)
            if not property:
                return request.render("website.404")
            return request.render(
                "estate.estate_property_details", {"property": property}
            )
        else:
            page = int(request.params.get("page", 1))
            properties_count = request.env["estate.property"].search_count([])
            total_pages = (properties_count // per_page) + (
                1 if properties_count % per_page > 0 else 0
            )
            properties = request.env["estate.property"].search(
                [], limit=per_page, offset=(page - 1) * per_page
            )
            return request.render(
                "estate.estate_properties",
                {
                    "properties": properties,
                    "current_page": page,
                    "total_pages": total_pages,
                },
            )
