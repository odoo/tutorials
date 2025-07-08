from odoo.http import Controller, request, route


class Property(Controller):

    @route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def fetch_all_properties(self, page=1):

        domain = [('state', 'not in', ['sold', 'canceled'])]
        properties_per_page = 6

        total_properties = request.env['estate.property'].sudo().search_count(domain)
        properties = request.env['estate.property'].sudo().search(domain, limit=properties_per_page, offset=(page - 1) * properties_per_page)

        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=properties_per_page
        )

        return request.render('estate.properties_template', {
            'properties': properties,
            'pager': pager
            })

    @route('/property/<int:id>', type='http', auth='public', website=True)
    def fetch_single_property(self, id=1):

        property = request.env['estate.property'].sudo().search([('id', '=', id)], limit=1)
        if not property:
            return request.not_found('Property does not exists')

        return request.render('estate.property_detail_template', {'property': property})
