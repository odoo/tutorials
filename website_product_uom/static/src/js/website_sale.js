/** @odoo-module **/

import { Component } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";

import { WebsiteSale } from "@website_sale/js/website_sale";
import wSaleUtils from "@website_sale/js/website_sale_utils";

let decimalPrecision = null;

async function getDecimalPrecision() {
    if (decimalPrecision !== null) {
        return decimalPrecision;
    }
    const precision = await rpc("/web/dataset/call_kw", {
        model: "decimal.precision",
        method: "search_read",
        args: [[["name", "=", "Product Unit of Measure"]], ["digits"]],
        kwargs: { limit: 1 },
    });
    decimalPrecision = precision.length ? precision[0].digits : 3;
    return decimalPrecision;
}

patch(WebsiteSale.prototype, {
    async _onClickAddCartJSON(ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0);
        var uomRatio = parseFloat($input.data("uom-ratio") || 1);
        var change = ($link.has(".fa-minus").length ? -1 : 1) * uomRatio;
        var quantity = previousQty + change;
        var minAllowed = Math.max(min, uomRatio);
        const decimals = await getDecimalPrecision();

        var newQty = parseFloat((Math.round(quantity / uomRatio) * uomRatio).toFixed(decimals));
        newQty = Math.max(minAllowed, Math.min(max, newQty));

        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    },

    async _changeCartQuantity($input, value, $dom_optional, line_id, productIDs) {
        const decimals = await getDecimalPrecision();
        value = parseFloat(value.toFixed(decimals));

        $($dom_optional).toArray().forEach((elem) => {
            $(elem).find('.js_quantity').text(value);
            productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
        });
        $input.data('update_change', true);

        rpc("/shop/cart/update_json", {
            line_id: line_id,
            product_id: parseInt($input.data('product-id'), 10),
            set_qty: value,
            display: true,
        }).then((data) => {
            $input.data('update_change', false);
            var check_value = parseFloat(parseFloat($input.val() || 0).toFixed(decimals));
            if (isNaN(check_value)) {
                check_value = 1;
            }
            if (value !== check_value) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return (window.location = '/shop/cart');
            }
            $input.val(parseFloat(data.quantity).toFixed(decimals));
            $('.js_quantity[data-line-id='+line_id+']').val(parseFloat(data.quantity).toFixed(decimals)).text(parseFloat(data.quantity).toFixed(decimals));

            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showWarning(data.notification_info.warning);
            // Propagating the change to the express checkout forms
            Component.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
        });
    },

    async _onChangeCartQuantity(ev) {
        var $input = $(ev.currentTarget);
        if ($input.data('update_change')) {
            return;
        }

        const decimals = await getDecimalPrecision();
        var value = parseFloat(parseFloat($input.val() || 0).toFixed(decimals));
        if (isNaN(value)) {
            value = 1;
        }
        var $dom = $input.closest('tr');
        var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
        var line_id = parseInt($input.data('line-id'), 10);
        var productIDs = [parseInt($input.data('product-id'), 10)];
        this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
    }
});
