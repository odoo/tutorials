from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):

    @http.route(['/offer', "/estate/page/property/<int:property_id>/offer", "/property/<int:property_id>/offer"], auth='public', type='http', website=True)
    def estate_property_offer(self, property_id):
        property = request.env['estate.property'].browse(property_id)
        return request.render('estate_auction.make_offer_template', {'property': property})

    @http.route(['/properties', '/properties/<int:property_id>', '/properties/page/<int:page>'], type='http', methods=['GET'], auth='public', website=True, csrf=False)
    def list_properties(self, property_id=None, page=1, **kargs):
        # if property_id found then render property details
        if property_id:
            property = request.env['estate.property'].browse(property_id)
            return request.render('estate.property_detail_template', {'property': property})

        # if property_id not found then render all property list
        page_size = 6
        offset = (int(page) - 1) * page_size  # offset == index of properties array to start fatching
        properties = request.env['estate.property'].search([('state', 'in', ('new', 'offer_received'))], limit=page_size, offset=offset)
        total_properties = request.env['estate.property'].search_count([('state', 'in', ('new', 'offer_received'))])

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=page_size
        )
        return request.render('estate.property_list_template', {'properties': properties, 'pager': pager})

    @http.route([
        '/properties/<string:sale_type>',
        '/properties/<string:sale_type>/page/<int:page>',
    ], type='http', auth='public', website=True, csrf=False)
    def list_filtered_properties(self, sale_type=None, property_id=None, page=1, **kwargs):
        # Filter for listing properties

        domain = [('state', 'in', ('new', 'offer_received'))]
        if sale_type in ['auction', 'regular']:
            domain.append(('sale_type', '=', sale_type))

        page_size = 6
        offset = (int(page) - 1) * page_size

        properties = request.env['estate.property'].search(domain, limit=page_size, offset=offset)
        total_properties = request.env['estate.property'].search_count(domain)

        base_url = f"/properties/{sale_type}" if sale_type else "/properties"

        pager = request.website.pager(
            url=base_url,
            total=total_properties,
            page=page,
            step=page_size
        )

        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager,
            'sale_type': sale_type,
        })
