from datetime import date
from odoo import http
from odoo.http import request


class VendorPortal(http.Controller):

    @http.route(['/vendor-portal', '/vendor-portal/page/<int:page>'], type='http', auth="user", website=True)
    def vendor_portal(self, vendor_country=None, vendor_id=None, category_id=None, product_name=None, page=1, **kwargs):
        env = request.env
        per_page = 15
        offset = (int(page) - 1) * per_page
        domain = []
        if vendor_country:
            domain.append(('seller_ids.partner_id.country_id', '=', int(vendor_country)))
        if vendor_id:
            domain.append(('seller_ids.partner_id', '=', int(vendor_id)))
        if category_id:
            domain.append(('categ_id', '=', int(category_id)))
        if product_name:
            domain.append(('name', 'ilike', product_name))

        Product = env['product.template'].sudo()
        total_products = Product.search_count(domain)
        products = Product.search(domain, order="name asc", offset=offset, limit=per_page)
        matching_products = Product.search([('name', 'ilike', product_name or '')], order="name asc").mapped("name")
        product_data = [{
            'id': product.id,
            'name': product.name,
            'image_url': f"/web/image/product.template/{product.id}/image_1920",
            'min_price': min([vendor.price for vendor in product.seller_ids if vendor.price] or [0]),
            'max_price': max([vendor.price for vendor in product.seller_ids if vendor.price] or [0]),
            'vendors': [
                {'id': vendor.partner_id.id, 'name': vendor.partner_id.name, 'price': vendor.price}
                for vendor in product.seller_ids if vendor.partner_id.active
            ]
        } for product in products]

        SupplierInfo = env['product.supplierinfo'].sudo()
        vendor_country_ids = SupplierInfo.search([]).mapped('partner_id.country_id.id')
        countries = env['res.country'].sudo().search([('id', 'in', vendor_country_ids)], order="name asc")
        vendor_ids = SupplierInfo.search([]).mapped('partner_id.id')
        vendors = env['res.partner'].sudo().browse(vendor_ids).sorted(key=lambda v: v.name)
        categories = env['product.category'].sudo().search([], order="name asc")
        url_args = {
            'vendor_country': vendor_country or '',
            'vendor_id': vendor_id or '',
            'category_id': category_id or '',
            'product_name': product_name or ''
        }
        pager = request.website.pager(
            url="/vendor-portal",
            total=total_products,
            page=int(page),
            step=per_page,
            scope=5,
            url_args=url_args
        )
        return request.render("custom_vendor_portal.vendor_portal_template", {
            'products': product_data,
            'countries': countries,
            'vendors': vendors,
            'categories': categories,
            'selected_country': int(vendor_country) if vendor_country else None,
            'selected_vendor': int(vendor_id) if vendor_id else None,
            'selected_category': int(category_id) if category_id else None,
            'search_product': product_name or '',
            'matching_products': matching_products,
            'pager': pager
        })

    @http.route('/create-purchase-order', type='http', auth='user', methods=['POST'])
    def create_purchase_order(self, **post):
        product_tmpl_id = post.get('product_id')
        vendor_id = post.get('vendor_id')
        quantity = int(post.get('quantity', 1))

        if not product_tmpl_id or not vendor_id or quantity <= 0:
            return request.redirect('/vendor-portal?error=missing_data')

        env = request.env
        product_tmpl_id, vendor_id = int(product_tmpl_id), int(vendor_id)
        product = env['product.product'].sudo().search([('product_tmpl_id', '=', product_tmpl_id)], limit=1)
        vendor = env['res.partner'].sudo().browse(vendor_id)
        supplier_info = env['product.supplierinfo'].sudo().search([
            ('product_tmpl_id', '=', product_tmpl_id),
            ('partner_id', '=', vendor_id)
        ], limit=1)
        price = supplier_info.price if supplier_info else product.standard_price
        existing_po = env['purchase.order'].sudo().search([
            ('partner_id', '=', vendor.id),
            ('state', '=', 'draft'),
            ('create_uid', '=', env.user.id)
        ], limit=1)

        if existing_po:
            order_line = existing_po.order_line.filtered(lambda l: l.product_id.id == product.id)
            if order_line:
                order_line.sudo().write({'product_qty': order_line.product_qty + quantity, 'price_unit': price})
            else:
                env['purchase.order.line'].sudo().create({
                    'order_id': existing_po.id,
                    'product_id': product.id,
                    'product_qty': quantity,
                    'price_unit': price
                })
            po_id = existing_po.id
        else:
            po_id = env['purchase.order'].sudo().create({
                'partner_id': vendor.id,
                'date_order': date.today(),
                'create_uid': env.user.id,
                'order_line': [(0, 0, {'product_id': product.id, 'product_qty': quantity, 'price_unit': price})]
            }).id

        return request.redirect(f'/vendor-portal?success=po_created&po_id={po_id}')
