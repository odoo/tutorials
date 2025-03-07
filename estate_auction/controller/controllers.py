from odoo import http
from odoo.http import request
from odoo.addons.estate.controller.controllers import Estate 


class EstateAuction(Estate):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, **kwargs):
        Property = request.env['estate.property']  

        domain = [('state', 'in', ['new', 'offer_received'])]

        listed_after = kwargs.get('listed_after')
        if listed_after:
            domain.append(('create_date', '>=', listed_after))

        selling_method = kwargs.get('selling_method')
        if selling_method:
            domain.append(('selling_method', '=', selling_method))

        properties_count = Property.search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=6,
            url_args={'listed_after': listed_after, 'selling_method': selling_method} if listed_after or selling_method else {}
        )

        properties = Property.search(domain, limit=6, offset=pager['offset'])

        return request.render('estate.property_listing', {
            'properties': properties,
            'pager': pager,
            'listed_after': listed_after or '',
            'selling_method': selling_method or '',
        })
    @http.route('/property/<int:id>/add_offer', type='http', auth="public", website=True)
    def add_offer(self, id, **kwargs):
        property = request.env['estate.property'].sudo().browse(id)
        if not property:
            return request.not_found()
        return request.render('estate_auction.offer_form_template', {
            'property': property,
            'error': kwargs.get('error')
        })

    @http.route('/property/offer/submit', type='http', auth="user", website=True, csrf=False)
    def submit_offer(self, **kwargs):
        property_id = int(kwargs.get('property_id'))
        price = float(kwargs.get('price'))

        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if property_obj.exists() and property_obj.selling_method == 'auction':
            if price < property_obj.expected_price:
                return request.render('estate_auction.offer_form_template', {
                    'property': property_obj,
                    'error': "Offer price must be at least the expected price."
                })

        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'price': price,
            'partner_id': request.env.user.partner_id.id,
        })

        return request.render('estate_auction.offer_success_template')
