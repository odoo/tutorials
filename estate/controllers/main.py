from odoo.http import Controller, request, route


class EstatePropertyController(Controller):
    _references_per_page = 3
    # Route For all properties
    @route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
        Property = request.env['estate.property']
        PropertyType = request.env['estate.property.type']

        property_types = PropertyType.sudo().search([])
        selected_type = kwargs.get('property_type')

        domain = [('state', 'in', ['new', 'offer_received'])]
        if selected_type:
            domain.append(('property_type_id', '=', int(selected_type)))

        property_count = Property.sudo().search_count(domain)

        pager = request.website.pager(
            url='/properties',
            total=property_count,
            page=page,
            step=self._references_per_page,
        )

        properties = Property.search(
            domain,
            offset=pager['offset'],
            limit=self._references_per_page
        )

        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager,
            'property_types': property_types,
            'selected_type': int(selected_type) if selected_type else None
        })

    # Route For Particular Property
    @route(['/properties/<int:property_id>/'], type='http', auth="public", website=True)
    def list_property_details(self, property_id, **kwargs):
        property_details = request.env['estate.property'].sudo().browse(property_id)
        return request.render('estate.property_detail_template', {
            'property_details': property_details
        })
