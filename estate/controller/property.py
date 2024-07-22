from odoo.http import route, Controller, request


class Propertycontroller(Controller):
    @route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def properties(self, **kwargs):
        domain = [('state', 'not in', ['sold', 'canceled'])]
        page = int(kwargs.get('page', 0))
        total_properties = request.env["estate.property"].search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=6,
        )
        properties = request.env['estate.property'].search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.property_template', {
            'properties': properties,
            'pager': pager,
            })

    @route('/property/<model("estate.property"):property_obj>', type='http', auth='public', website=True)
    def property_detail(self, property_obj, **kwargs):
        return request.render('estate.property_detail', {
            'property': property_obj,
        })
