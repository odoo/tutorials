from odoo.http import request, route, Controller


class RealEstateController(Controller):
    @route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website="True",
    )
    def property_list(self, **kwarg):
        domain = [("state", "not in", ["sold", "canceled"])]
        page = int(kwarg.get("page", 1))
        total_properties = request.env["estate.property"].search_count(domain)

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=4,
        )

        properties = request.env["estate.property"].search(
            domain, limit=6, offset=pager["offset"]
        )
        return request.render(
            "estate.properties_page", {"properties": properties, "pager": pager}
        )

    @route("/properties/<int:property_id>", type="http", auth="public", website="True")
    def property_detail_page(self, property_id, **kwarg):
        property_record = request.env["estate.property"].browse(property_id)
        return request.render(
            "estate.property_detail_page", {"property": property_record}
        )
