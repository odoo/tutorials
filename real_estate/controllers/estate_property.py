from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
        """ Display properties with pagination and optional search """
        properties_per_page = 6
        domain = []

        search_query = kwargs.get('search', '').strip()
        if search_query:
            domain += ['|', ('name', 'ilike', search_query), ('description', 'ilike', search_query)]

        total_properties = request.env['estate.property'].sudo().search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=properties_per_page,
            url_args={'search': search_query} if search_query else {}
        )

        properties = request.env['estate.property'].sudo().search(
            domain,
            offset=pager['offset'],
            limit=properties_per_page
        )

        return request.render('real_estate.website_property_template', {
            'properties': properties,
            'pager': pager,
            'search_query': search_query
        })

    @http.route(['/properties/<int:property_id>'], type='http', auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        """ Display detailed view of a single property """
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render('real_estate.property_detail_template', {'property': property})

    @http.route('/properties/<int:property_id>/make-offer', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def make_offer(self, property_id, **body):
        property = request.env['estate.property'].sudo().browse(property_id)

        if not property.exists():
            return request.redirect('/properties')

        offer_price = body.get('offer_price')
        date_validity = body.get('date_validity')
        # Get logged-in user's partner
        partner = request.env.user.partner_id

        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': partner.id,
            'price': float(offer_price),
            'date_deadline': date_validity,
        })
        return request.redirect('/properties/%d' % property_id)
