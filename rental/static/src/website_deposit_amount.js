import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.Rental = publicWidget.Widget.extend({
    selector: "#product_detail",
    events: {
           'change input[type="text"]': '_updateDepositAmount',
    },

    start: function () {
        this._super.apply(this, arguments);
        this._perUnitDeposit = $("#deposit_amount").text()?? 0;
        if ($("#deposit_amount").length && ($("#deposit_amount").text()?? 0) > 0) {
            this._updateDepositAmount(); 
        } else {
            this.$el.off('change input[name="add_qty"]');
        }
    },

    _updateDepositAmount(event) {   
        var qty = parseFloat($("#o_wsale_cta_wrapper").find("input[name='add_qty']").val()) || 1;
        var depositAmount = parseFloat($("#deposit_amount").text()) || 0;
        if(Number(this._perUnitDeposit) !== 0)
            $("#deposit_amount").text(this._perUnitDeposit * (qty));  
    },
});
