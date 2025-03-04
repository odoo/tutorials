from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate_property_website import EstatePropertyWebsite


class EstatePropertyWebsiteInherited(EstatePropertyWebsite):
    @http.route(['/estate/properties/', '/estate/properties/page/<int:page>'], auth='public', website=True)
    def list_estate_properties(self, page=1, **kwargs):
        domain = [('state', 'in', ['new', 'offer_received'])]
        _url_arguments = {}

        if kwargs.get('min_price'):
            domain.append(('expected_price', '>=', float(kwargs['min_price'])))
            _url_arguments['min_price'] = kwargs['min_price']

        if kwargs.get('max_price'):
            domain.append(('expected_price', '<=', float(kwargs['max_price'])))
            _url_arguments['max_price'] = kwargs['max_price']

        if kwargs.get('auction') == 'yes':
            domain.append(('sale_type', '=', 'auction'))
            _url_arguments['auction'] = 'yes'
        elif kwargs.get('auction') == 'no':
            domain.append(('sale_type', '!=', 'auction'))
            _url_arguments['auction'] = 'no'

        if kwargs.get('listed_after'):
            domain.append(('create_date', '>=', kwargs['listed_after']))
            _url_arguments['listed_after'] = kwargs['listed_after']

        if kwargs.get('status'):
            if kwargs['status'] == 'all':
                domain[0] = ('state', 'in', ['new', 'offer_received', 'sold', 'offer_accepted'])
                _url_arguments['status'] = kwargs['status']
            elif kwargs['status'] == 'alls':
                domain = []
            else:
                domain[0] = ('state', '=', kwargs['status'])
                _url_arguments['status'] = kwargs['status']

        properties = request.env['estate.property'].sudo().search(
            domain, order='create_date desc'
        )

        _items_per_page = 6
        _total = len(properties)
        _starting_index = (page - 1) * _items_per_page
        _page_properties = properties[_starting_index: _starting_index + _items_per_page]

        pager = request.website.pager(
            url='/estate/properties',
            total=_total,
            page=page,
            step=_items_per_page,
            scope=4,
            url_args=_url_arguments
        )

        return request.render('estate.estate_properties_website', {
            'pager': pager,
            'properties': _page_properties,
            'status': kwargs.get('status', ''),
            'min_price': kwargs.get('min_price', ''),
            'max_price': kwargs.get('max_price', ''),
            'auction': kwargs.get('auction', ''),
            'listed_after': kwargs.get('listed_after', '')
        })

class EstatePropertyAuctionWebsite(http.Controller):
    @http.route('/estate/property/<int:property_id>/create_offer', type='http', auth="public", website=True)
    def create_offer(self, property_id, **kwargs):
        property_record = request.env['estate.property'].sudo().browse(property_id)
        print(f'{property_record.state}')
        if not property_record.exists():
            return request.redirect('/estate/properties')

        elif property_record.sale_type != 'auction' or property_record.state in ['offer_accepted', 'sold'] or property_record.auction_state in ['sold']:
            return request.redirect('/estate/property/%s' % property_id)

        return request.render('estate_auction.estate_property_offer_form', {
            'property': property_record
        })

    @http.route('/estate/property/submit_offer', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def submit_offer(self, **kwargs):
        try:
            property_id = int(kwargs.get('property_id'))
            buyer_name = kwargs.get('buyer_name')
            buyer_id = request.env['res.partner'].sudo().search([('name', '=', buyer_name)], limit=1).id
            offer_amount = float(kwargs.get('offer_amount'))

            property_obj = request.env['estate.property'].sudo().browse(property_id)
            if property_obj.exists() and property_obj.sale_type == 'auction':
                if offer_amount < property_obj.expected_price:
                    return request.render('estate_auction.estate_property_offer_form', {
                        'property': property_obj,
                        'error': "Offer price must be at least the expected price."
                    })

                request.env['estate.property.offer'].sudo().create({
                    'property_id': property_id,
                    'partner_id': buyer_id,
                    'price': offer_amount,
                })

            return request.render('estate_auction.estate_property_offer_success', {
                'property': request.env['estate.property'].sudo().browse(property_id),
            })

        except Exception as e:
            return request.render('estate_auction.estate_property_offer_form', {
                'error': str(e)
            })
