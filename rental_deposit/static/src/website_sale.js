import { WebsiteSale } from "@website_sale/js/website_sale";

WebsiteSale.include({
    _onClickAddCartJSON(ev) {
        this._super(...arguments);
        this._updateDepositTotal();
    },

    _onChangeAddQuantity(ev) {
        this._super(...arguments);
        this._updateDepositTotal();
    },

    _updateDepositTotal() {
        const qtyInput = document.querySelector('input[name="add_qty"]');
        const qty = parseInt(qtyInput?.value || 1);
        const depositValueEl = document.querySelector('#deposit_base_amount');
        const depositTotalEl = document.querySelector('#deposit_total_amount');
        const quantity = document.querySelector('#deposit_quantity')

        if (depositValueEl && depositTotalEl) {
            const deposit = parseFloat(depositValueEl.textContent) || 0;
            const total = qty * deposit;
            depositTotalEl.textContent = total.toFixed(2);
            quantity.textContent = qty;
        }
    },
})
