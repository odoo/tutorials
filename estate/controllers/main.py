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
            url="/properties",
            total=len(found_properties),
            page=page,
            step=self._property_per_page,
            url_args=kwargs,
        )

        offset = pager["offset"]
        properties_list = found_properties[offset: offset + self._property_per_page]

        return request.render(
            "estate.estate_properties_template",
            {
                "properties": properties_list,
                "pager": pager,
            }
        )

    @route(
        ['/properties/<int:property_id>'],
        type='http',
        auth='public',
        website=True
    )
    def property_detail(self, property_id, **kwargs):

        property_record = request.env[
            'estate.property'
        ].sudo().browse(property_id)

        return request.render(
            'estate.estate_property_detail_template',
            {
                'property': property_record
            }
        )
