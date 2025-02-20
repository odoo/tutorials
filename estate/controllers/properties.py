# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import http
from odoo.http import request

class PropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type="http", auth="public", website=True)
    def properties(self, page=1, **kwargs):
        property_model = request.env['estate.property']
        filter = [('state', 'not in', ['sold', 'cancelled'])]
        properties_count = property_model.search_count(filter)
        per_page = 4    

        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=per_page
        )

        properties = property_model.search(filter, offset=(page - 1) * per_page, limit=per_page)

        return request.render("estate.estate_property_list", {  
            'properties': properties,
            'pager': pager
        })

    @http.route('/properties/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id):
        property_record = request.env['estate.property'].browse(property_id)

        if not property_record.exists():
            return request.render('Not Found')

        return request.render('estate.property_detail_template', {
            'property': property_record
        })

    @http.route('/offer/create', auth='user', methods=['POST'], website=True)
    def create_offer(self, **kw):
        property_id = int(kw.get('property_id'))
        price = float(kw.get('price'))
        
        property_record = request.env['estate.property'].browse(property_id)
        max_offer = max(property_record.property_offer_ids.mapped('price'), default=0)

        if price <= max_offer:
            return request.redirect(f'/properties/{property_id}?error=Offer must be higher than {max_offer}')

        offer = request.env['estate.property.offer'].create({
            'partner_id': request.env.user.partner_id.id,
            'property_id': property_id,
            'price': price,
        })
        return request.redirect(f'/properties/{property_id}')
