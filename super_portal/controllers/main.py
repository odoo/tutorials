from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden

class WebsiteSalePortal(WebsiteSale):

    #-------------------------------------------------------------------------------#
    # Arrange branches in order the display of address options available
    #-------------------------------------------------------------------------------#
    def checkout_values(self, order, **kw):
        order = order or request.website.sale_get_order(force_create=True)
        bill_partners = []
        ship_partners = []

        if not order._is_public_order():
            Partner = order.partner_id.with_context(show_address=1).sudo()
            commercial_partner = order.partner_id.commercial_partner_id
            bill_partners = Partner.search([
                '|', ("type", "in", ["invoice", "other"]), ("id", "=", commercial_partner.id),
                ("id", "child_of", commercial_partner.ids)
            ], order='id asc, parent_id asc') | order.partner_id
            ship_partners = Partner.search([
                '|', ("type", "in", ["delivery", "other"]), ("id", "=", commercial_partner.id),
                ("id", "child_of", commercial_partner.ids)
            ], order='id asc, parent_id asc') | order.partner_id

            if commercial_partner != order.partner_id:
                if not self._check_billing_partner_mandatory_fields(commercial_partner):
                    bill_partners = bill_partners.filtered(lambda p: p.id != commercial_partner.id)
                if not self._check_shipping_partner_mandatory_fields(commercial_partner):
                    ship_partners = ship_partners.filtered(lambda p: p.id != commercial_partner.id)

        return {
            'order': order,
            'website_sale_order': order,
            'shippings': ship_partners,
            'billings': bill_partners,
            'only_services': order and order.only_services or False
        }

    #----------------------------------------------------------------------------------------------#
    # Recompute the prices according to the price list associated with the selected billing address
    #----------------------------------------------------------------------------------------------#
    @http.route(
        '/shop/cart/update_address', type='http', auth='public',
        methods=['POST'], website=True, csrf=False
    )
    def update_cart_address(self, partner_id, mode='billing', **kw):
        response = super().update_cart_address(partner_id, mode, **kw)

        order_sudo = request.website.sale_get_order()
        if not order_sudo:
            return response

        partner_sudo = request.env['res.partner'].sudo().browse(int(partner_id)).exists()
        if not partner_sudo:
            raise Forbidden()

        new_pricelist = partner_sudo.property_product_pricelist
        if new_pricelist and new_pricelist != order_sudo.pricelist_id:
            order_sudo.write({'pricelist_id': new_pricelist.id})

        order_sudo._recompute_prices()
        order_sudo._compute_amounts()
        order_sudo.sudo().write({
            'amount_total': order_sudo.amount_total,
            'amount_tax': order_sudo.amount_tax,
            'amount_untaxed': order_sudo.amount_untaxed
        })

        return response

    @http.route(
        ['/shop/cart/update_total'], type='json', auth='public',
        methods=['POST'], website=True, csrf=False
    )
    def cart_update_total(self):
        order_sudo = request.website.sale_get_order()
        if not order_sudo:
            return {"error": "No active order found"}

        line_items = [
            {
                "unit_price": line.price_unit,
                "subtotal": line.price_subtotal,
            }
            for line in order_sudo.order_line
        ]

        return {
            "amount_untaxed": order_sudo.amount_untaxed,
            "amount_tax": order_sudo.amount_tax,
            "amount_total": order_sudo.amount_total,
            "cart_quantity": order_sudo.cart_quantity,
            "line_items": line_items,
        }

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True, sitemap=False)
    def confirm_order(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order) or self.checkout_check_address(order)
        if redirection:
            return redirection

        order.order_line._compute_tax_id()
        # Disable to update pricelist based on Website Pricelist

        # request.website.sale_get_order(update_pricelist=True)
        extra_step = request.website.viewref('website_sale.extra_info')
        if extra_step.active:
            return request.redirect("/shop/extra_info")

        return request.redirect("/shop/payment")
