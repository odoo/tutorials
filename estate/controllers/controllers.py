from odoo.http import Controller, route, request


class EstateWebsite(Controller):
    _property_per_page = 6

    @route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True)
    def properties(self, page=1, **kwargs):
        website = request.website

        found_properties = request.env["estate.property"].sudo().search([])
        pager = website.pager(
            url=request.httprequest.path.partition("/page/")[0],
            total=len(found_properties),
            page=page,
            step=self._property_per_page,
        )
        offset = pager["offset"]
        properties_list = found_properties[
            offset : offset + self._property_per_page
        ]

        return request.render("estate.estateproperties", {"properties": properties_list, "pager": pager})

    @route(
        "/properties/<int:property_id>",
        type="http",
        auth="public",
        website=True)
    def property_detail(self, property_id, **kwargs):
        property_obj = request.env["estate.property"].browse(property_id)
        return request.render("estate.estatepropertydetail", {"property": property_obj})
