from odoo.http import Controller, request, route


class PropertyListController(Controller):

    @route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1):
        Property = request.env['estate.property'].sudo()
        total_properties = Property.search_count([])
        properties_per_page = 6
        offset_value = (page - 1)*properties_per_page
        properties = Property.search([], limit=properties_per_page, offset=offset_value)

        return request.render('estate.property_listing_template', {
            'properties': properties,
            'pager': request.website.pager(
                url='/properties',
                total=total_properties,
                page=page,
                step=properties_per_page
            )
        })

    @route('/property/filter', type='http', auth='public', website=True)
    def property_filter(self, selected_date=None, query=None):
        if selected_date:
            properties = request.env['estate.property'].search([('create_date', '>=', selected_date)], order="create_date DESC")
            if properties:
                return request.render('estate.property_listing_template', {
                    'properties': properties
                })
            else:
                return request.not_found()
        elif query:
            properties = request.env['estate.property'].search([('name', 'ilike', query)])
            if properties:
                return request.render('estate.property_listing_template', {
                    'properties': properties
                })
            else:
                return request.not_found()

    @route('/property/detail/<int:id>', type='http', auth='public', website=True)
    def property_detail(self, id):
        property = request.env['estate.property'].search([('id', '=', id)])
        if property:
            return request.render('estate.property_detail_template', {
                'property': property
            })
        else:
            return request.not_found()
