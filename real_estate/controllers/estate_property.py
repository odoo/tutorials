from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.tools.float_utils import float_compare

class EstatePropertyController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
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

    @http.route(['/properties/<int:property_id>'], type='http', auth="user", website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render('real_estate.property_detail_template', {'property': property})

    @http.route('/properties/<int:property_id>/make-offer', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def make_offer(self, property_id, **body):
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.redirect('/properties')

        offer_price = body.get('offer_price')
        date_validity = body.get('date_validity')
        partner = request.env.user.partner_id
        best_price=property.best_price

        if float_compare(float(best_price), float(offer_price), 2) == 1:
            return request.render('real_estate.property_detail_template', {
                'error': f"We are not accepting offer below ₹{best_price}",
                'property': property
            })

        if date_validity and datetime.strptime(date_validity, "%Y-%m-%d").date() < datetime.now().date():
            return request.render('real_estate.property_detail_template', {
                'error': "The offer deadline must be today or later.",
                'property': property
            })

        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': partner.id,
            'price': float(offer_price),
            'date_deadline': date_validity,
        })
        return request.redirect('/properties/%d' % property_id)
