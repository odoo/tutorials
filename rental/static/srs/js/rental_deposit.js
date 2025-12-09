import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSale.include({
    start: function () {
        this._super.apply(this, arguments);
        this.changeDepositAmount({ target: document.querySelector('input[name="add_qty"]') });
    },

    _onChangeAddQuantity: function (ev) {
        this._super.apply(this, arguments);
        this.changeDepositAmount(ev);
    },

    changeDepositAmount: function(ev){
        const input = ev.target || document.querySelector('input[name="add_qty"]');
        if (!input) return;
        const qty = parseFloat(input.value || 1);
        const depositSpan = document.getElementById('product_amount_deposit');
        if (!depositSpan) return;

        const baseDeposit = parseFloat(depositSpan.dataset.baseAmount || 0);
        const currencySymbol = depositSpan.dataset.currencySymbol || '';
        const totalDeposit = (baseDeposit * qty).toFixed(2);
        depositSpan.textContent = `${currencySymbol} ${totalDeposit}`;
    }
});
