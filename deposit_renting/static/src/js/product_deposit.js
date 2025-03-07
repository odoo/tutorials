import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSale.include({
    _onChangeAddQuantity: function (ev) {
        this._super.apply(this, arguments);
        this.changeDepositAmount(ev);
    },

    changeDepositAmount: function(ev){
        const input = ev.target;
        const qty = parseFloat(input.value || 1);
        const depositSpan = document.getElementById('product_deposit_amount');
        if (!depositSpan) return;

        const baseDeposit = parseFloat(depositSpan.dataset.baseAmount || 0);
        const currencySymbol = depositSpan.dataset.currencySymbol || '';
        const totalDeposit = (baseDeposit * qty).toFixed(2);
        depositSpan.textContent = `${currencySymbol} ${totalDeposit}`;
    }
})
