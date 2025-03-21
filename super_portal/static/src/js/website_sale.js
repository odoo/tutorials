/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.websiteSaleCart = publicWidget.registry.websiteSaleCart.extend({
    events: Object.assign({}, publicWidget.registry.websiteSaleCart.prototype.events, {
        'click .js_change_billing': '_onClickChangeBilling',
    }),

    _onClickChangeBilling: function (ev) {
        var self = this;
        var rowAddrClass = "all_billing";
        var cardClass = "js_change_billing";

        var $old = $(`.${rowAddrClass}`).find('.card.border.border-primary');
        $old.find('.btn-addr').toggle();
        $old.addClass(cardClass);
        $old.removeClass('bg-primary border border-primary');

        var $new = $(ev.currentTarget).parent('div.one_kanban').find('.card');
        $new.find('.btn-addr').toggle();
        $new.removeClass(cardClass);
        $new.addClass('bg-primary border border-primary');

        var $form = $(ev.currentTarget).parent('div.one_kanban').find('form.d-none');
        $.post($form.attr('action'), $form.serialize() + '&xhr=1').done(function () {
            self._updateCartTotals();
        });
    },

    _updateCartTotals: function () {
        jsonrpc("/shop/cart/update_total", {})
            .then((data) => {
                if (!data.cart_quantity) {
                    return window.location.reload();
                }
                $("#order_total_untaxed .oe_currency_value").html(data.amount_untaxed.toFixed(2));
                $("#order_total_taxes .oe_currency_value").html(data.amount_tax.toFixed(2));
                $("#order_total .oe_currency_value").html(data.amount_total.toFixed(2));
                $("#amount_total_summary .oe_currency_value").html(data.amount_total.toFixed(2));

                let $cartRows = $("#cart_products tr");
                data.line_items.forEach((line, index) => {
                    let $row = $cartRows.eq(index);
                    $row.find(".oe_currency_value").text(line.subtotal.toFixed(2));
                });
            })
            .catch((err) => {
                console.error("Error updating cart totals:", err);
            });
    }
});
