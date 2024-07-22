from odoo.http import route, request, Controller


class TermsController(Controller):

    @route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def terms_conditions(self, page=1, **kwargs):
        domain = [('state', 'not in', ['sold', 'canceled'])]
        total_properties = request.env["estate.property"].search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=6,
        )
        properties = request.env['estate.property'].search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.available_properties', {
            'properties': properties,
            'pager': pager,
        })

    @route('/property/<model("estate.property"):property_obj>', type='http', auth='public', website=True)
    def property(self, property_obj, **kwargs):
        return request.render('estate.property_template', {
            'property': property_obj,
        })
