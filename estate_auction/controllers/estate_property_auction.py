from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate_property import EstatePropertyController


class EstatePropertyAuctionController(EstatePropertyController):

    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True, type='http')
    def list_properties(self, page=1, **kwargs):
        domain = [('state', 'in', ['new', 'offer_accepted', 'offer_received'])]
        listed_date = kwargs.get('listed_date')
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        sale_type = kwargs.get('sale_type')

        if min_price:
            try:
                domain.append(('expected_price', '>=', float(min_price)))
            except ValueError:
                min_price = None

        if max_price:
            try:
                domain.append(('expected_price', '<=', float(max_price)))
            except ValueError:
                max_price = None

        if listed_date:
            try:
                listed_date = datetime.strptime(listed_date, '%Y-%m-%d').date()
                domain.append(('create_date', '>=', listed_date))
            except ValueError:
                listed_date = None

        if sale_type:
            try:
                domain.append(('sale_type', '=', sale_type))
            except ValueError:
                sale_type = None

        url_args = kwargs
        properties_per_page = 6
        offset = (int(page) -1) * properties_per_page
        total_properties = request.env['estate.property'].sudo().search_count(domain)

        properties = request.env['estate.property'].sudo().search(
            domain,
            order='create_date desc',
            limit=properties_per_page,
            offset=offset
        )
        pager = request.website.pager(
            url = "/properties",
            total = total_properties,
            page = page,
            step = properties_per_page,
            scope = 3,
            url_args = url_args
        )
        return request.render('estate.estate_property_template', {
            'properties': properties,
            'pager': pager,
            'min_price': min_price,
            'max_price': max_price,
            'listed_date': listed_date,
            'sale_type': sale_type,
        })

    @http.route('/property/<int:property_id>/offer/new', auth='user', website=True, type='http')
    def property_offer_add(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()
        user = request.env.user.name
        return request.render('estate_auction.property_offer_template', {
            'property_id' : property_id,
            'name': user
        })

    @http.route('/property/<int:property_id>/offer/submit', auth='user', website=True, type='http')
    def property_offer(self,property_id, price=None, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()
        if price and float(price) >= property_obj.expected_price:
            success = True
            vals_list = [{
                'property_id' : property_id,
                'partner_id' : request.env.user.partner_id.id,
                'price' : float(price)
            }]
            property_obj.property_offer_ids.create(vals_list)
        else:
            success = False
        return request.render('estate_auction.property_offer_status_template', {
            'property_id' : property_id,
            'success': success
        })
