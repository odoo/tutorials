import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.DepositRental = publicWidget.Widget.extend({
    selector: "#product_detail",
    events: {
        'change input[name="add_qty"]': '_updateDepositAmount',
    },
    start: function () {
        this._super.apply(this, arguments);
        if ($("#deposit_amount").length && $("#deposit_amount").data("base-amount") > 0) {
            this._updateDepositAmount(); 
        } else {
            this.$el.off('change input[name="add_qty"]');
        }
    },
    _updateDepositAmount: function () {
        var qty = parseFloat($("#o_wsale_cta_wrapper").find("input[name='add_qty']").val()) || 1;
        var depositAmount = parseFloat($("#deposit_amount").data("base-amount")) || 0;
        $("#deposit_amount").text(depositAmount * qty);
    }
});
