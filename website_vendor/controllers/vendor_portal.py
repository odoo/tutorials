import json
from odoo import http
from odoo.http import request


class VendorPortal(http.Controller):

    @http.route('/vendor_portal', type='http', auth="user", website="true", methods=['GET'])
    def renderVendorPortal(self, country=None, vendor=None, category=None, product=None):
        Categories = request.env['product.category'].search([]).mapped('name')
        Countries = request.env['res.country'].search([]).mapped('name')
        Products = request.env['product.template'].search([]).mapped('name')
        Vendors = request.env['product.supplierinfo'].search([]).mapped('partner_id.name')

        domain = [('purchase_ok', '=', True)]

        if category:
            category_id = request.env['product.category'].search(
                [('name', '=ilike', category)], limit=1
            ).id
            if category_id:
                domain.append(('categ_id', '=', category_id))

        if country:
            country_id = request.env['res.country'].search(
                [('name', '=ilike', country)], limit=1
            ).id
            if country_id:
                domain.append(
                    ('seller_ids.partner_id.country_id', '=', country_id)
                )

        if product:
            domain.append(('name', 'ilike', product))

        if vendor:
            vendor_id = request.env['res.partner'].search(
                [('name', '=ilike', vendor)], limit=1
            ).id
            if vendor_id:
                domain.append(('seller_ids.partner_id', '=', vendor_id))

        search_result = request.env['product.template'].search(
            domain, order='name asc'
        )

        product_vendor_list = {}

        if search_result:
            for p in search_result:
                product_vendor_list[p.id] = json.dumps([
                    {
                        'vendor_id': vendor.partner_id.id, 
                        'vendor_name': vendor.partner_id.name, 
                        'min_qty': vendor.min_qty,
                        'price': vendor.price,
                    } for vendor in p.seller_ids
                ])

        return request.render('website_vendor.website_vendor_portal_template', {
            'countries': Countries,
            'vendors': Vendors,
            'categories': Categories,
            'products': Products,
            'search_result': search_result,
            'product_vendor_list': product_vendor_list,
        })
