# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class EstateController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kw):
        per_page = 3
        domain = ['&', ('active', '=', 'True'), ('state', 'not in', ['cancelled'])]
        total = request.env['estate.property'].sudo().search_count(domain)
        properties = request.env['estate.property'].sudo().search(
            domain,
            offset=(page - 1) * per_page,
            limit=per_page
        )
        pager = request.website.pager(
            url='/properties',
            total=total,
            page=page,
            step=per_page,
            scope=3
        )
        return request.render('estate.property_list_template', {
            'pager': pager,
            'properties': properties,
        })

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def view_property(self, property_id, **kw):
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()
        offers = request.env['estate.property.offer'].sudo().search([
            '&',
            ('property_id', '=', property_id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        max_offer = max(property.offer_ids.mapped('price')) if property.offer_ids else 0
        return request.render('estate.property_detail_template', {
            'property': property,
            'offers': offers,
            'max_offer': max_offer,
            'currency_symbol': request.env.company.currency_id.symbol,
        })

    @http.route('/offer/create', type='http', auth='user', methods=['POST'], website=True)
    def create_offer(self, **kw):
        property_id = int(kw.get('property_id'))
        request.env['estate.property.offer'].sudo().create({
            'partner_id': request.env.user.partner_id.id,
            'property_id': property_id,
            'price': float(kw.get('price')),
        })
        return request.redirect(f'/property/{property_id}')
