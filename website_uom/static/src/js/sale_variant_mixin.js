/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";

VariantMixin.onClickAddCartJSON = function (ev, ...change_qty) {
    ev.preventDefault();
    var $link = $(ev.currentTarget);
    var $input = $link.closest('.input-group').find("input");
    var min = parseFloat($input.data("min") || 0);
    var max = parseFloat($input.data("max") || Infinity);
    var previousQty = parseFloat($input.val() || 0, 10);
    if (change_qty.length != 0){
        var quantity = ($link.has(".fa-minus").length ? -change_qty[0] : change_qty[0]) + previousQty;
    }
    else {
        var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
    }
    var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
    if (newQty !== previousQty) {
        $input.val(newQty).trigger('change');
    }
    return false;
}
