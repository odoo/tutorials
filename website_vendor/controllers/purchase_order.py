from odoo import http
from odoo.http import request


class CreatePurchaseOrder(http.Controller):

    @http.route('/purchase_order_view', type='http', auth="user", website="true", methods=['POST'])
    def _on_create_purchase_order(self, **kwargs):
        product_id = int(kwargs.get('product_id'))
        vendor_id = int(kwargs.get('vendor_id'))
        quantity = int(kwargs.get('quantity'))

        if not product_id or not vendor_id or not quantity:
            return request.redirect('/')

        product_template = request.env['product.template'].browse(product_id)
        product = product_template.product_variant_id
        vendor = request.env['res.partner'].browse(vendor_id)
        
        company_id = (
            vendor.company_id.id 
            if vendor.company_id 
            else request.env.company.id
        )

        purchase_order = request.env['purchase.order'].search(
            [('partner_id', '=', vendor.id), ('state', '=', 'draft')],
            limit=1
        )

        if not purchase_order:
            purchase_order = request.env['purchase.order'].create({
                'partner_id': vendor.id,
                'company_id': company_id,
            })

        request.env['purchase.order.line'].create({
            'order_id': purchase_order.id,
            'product_qty': quantity,
            'product_id': product.id,
            'price_unit': product.min_price,
        })

        return request.render(
            'website_vendor.website_vendor_purchase_order_view',
            {
                'product_id': product,
                'vendor_id': vendor,
                'quantity': quantity,
            }
        )
