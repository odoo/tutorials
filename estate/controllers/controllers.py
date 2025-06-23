from odoo import http
from odoo.http import request, route


class EstateWebsite(http.Controller):
    @route(["/properties", "/properties/page/<int:page>"], auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
        properties_per_page = 6

        # Domain for available properties (new or offer_received)
        domain = [("state", "in", ["new", "offer_received"]), ("active", "=", True)]

        Property = request.env["estate.property"].sudo()
        property_count = Property.search_count(domain)

        # Configure pager
        pager = request.website.pager(
            url="/properties",
            total=property_count,
            page=page,
            step=properties_per_page,
        )

        # Get properties for current page
        properties = Property.search(
            domain,
            limit=properties_per_page,
            offset=pager["offset"],
            order="create_date desc",
        )

        values = {
            "properties": properties,
            "pager": pager,
        }

        return request.render("estate.property_list", values)

    @route(
        ['/properties/<model("estate.property"):property>'],
        auth="public",
        website=True,
    )
    def property_detail(self, property, **kwargs):
        if (
            not property
            or property.state in ["sold", "canceled"]
            or not property.active
        ):
            return request.redirect("/properties")

        return request.render(
            "estate.property_detail",
            {
                "property": property,
            },
        )
