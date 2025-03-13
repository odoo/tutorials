/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import { WebsiteSale } from '@website_sale/js/website_sale';

WebsiteSale.include({
    _onClickAddCartJSON: async function (ev){
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var change_qty = []
        const currentRoute = window.location.pathname;
        if (currentRoute.includes("/cart")) {
            var product_id = parseInt($link.closest('.o_cart_product').data('product-id'));
            change_qty = await rpc("/web/dataset/call_kw/product.template", {
                model: 'product.template',
                method: 'get_change_qty_from_product_id',
                args: [[product_id]],
                kwargs: {},
            })
        }
        else{
            var $parent = $link.closest('.js_product');
            var product_id = this._getProductId($parent);
            change_qty = await rpc("/web/dataset/call_kw/product.template", {
                model: 'product.template',
                method: 'get_change_qty_from_product_id',
                args: [[product_id]],
                kwargs: {},
            })
        }
        this.onClickAddCartJSON(ev, change_qty)
    }
})
