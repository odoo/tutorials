/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";


/**
 * Hack to add and remove from cart with json
 *
 * @param {MouseEvent} ev
 */
VariantMixin.onClickAddCartJSONNEW = function (ev) {
    console.log("jsssssssssssss")

    var $link = $(ev.currentTarget);
    var $input = $link.closest('.input-group').find("input");
    var min = parseFloat($input.data("min") || 0);
    var max = parseFloat($input.data("max") || Infinity);
    var previousQty = parseFloat($input.val() || 0, 10);
    var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
    var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

    var depositAmount = parseFloat($("#deposit_amount").text().trim() || 0);
    var updatedDeposit = (depositAmount/previousQty) * newQty;
    $("#deposit_amount").text(updatedDeposit.toFixed(2));
    
    if (newQty !== previousQty) {
        $input.val(newQty).trigger('change');
    }
    return false;
}

publicWidget.registry.WebsiteSale.include({
    /**
     * Update the renting text when the combination change.
     * @override
     */
    onClickAddCartJSON: function (){
        if(parseFloat($("#deposit_amount").text().trim())) {
            VariantMixin.onClickAddCartJSONNEW.apply(this, arguments);
        }
        else{
            this._super.apply(this, arguments)
        }    
    },
});

export default VariantMixin;

