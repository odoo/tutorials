from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def property_list(self, page=1, **kwargs):
        """Renders a list of all available properties"""
        Property = request.env["estate.property"].sudo()
        total_properties = Property.search_count([])  # Count total property

        property_per_page = 10  # Limit properties per page
        offset_val = (page - 1) * property_per_page
        properties = Property.search([], offset=offset_val, limit=property_per_page)

        custom_pager = request.website.pager(
            url="/properties", total=total_properties, page=page, step=property_per_page
        )
        return request.render(
            "estate.estate_property_list_template",
            {"properties": properties, "pager": custom_pager},
        )

    @http.route("/property/<int:property_id>", type="http", auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        property_obj = request.env["estate.property"].sudo().browse(property_id)
        if not property_obj.exists():
            return request.render("website.404")  # Redirect to 404 if not found

        return request.render(
            "estate.estate_property_details_template", {"property": property_obj}
        )
