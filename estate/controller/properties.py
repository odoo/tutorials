from odoo.http import request, route, Controller


class RealEstateController(Controller):

    @route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def list_properties(self, **kwargs):
        domain = [('state', 'not in', ['sold', 'canceled'])]
        page = int(kwargs.get('page', 0))
        total_properties = request.env["estate.property"].search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=6,
        )
        properties = request.env["estate.property"].search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.properties_page', {
            'properties': properties,
            'pager': pager,
        })

    @route('/property/<model("estate.property"):property_obj>', auth='user', website=True)
    def property_detail(self, property_obj, **kwargs):
        return request.render('estate.property_detail_page', {
            'property': property_obj
        })
