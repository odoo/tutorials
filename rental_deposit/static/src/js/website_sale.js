import { WebsiteSale } from "@website_sale/js/website_sale";

WebsiteSale.include({
    onClickAddCartJSON(ev) {
        const res = this._super(...arguments);
        const button = ev.currentTarget;
        const input = button.closest('.input-group').querySelector("input");
        const depositElem = document.querySelector(".deposit-amount");
        const depositAmt = parseFloat(depositElem.dataset.deposit || 0, 10);
        const qty = parseFloat(input.value || 0, 10);
        const newDepositAmt = depositAmt * qty;
        depositElem.textContent = newDepositAmt.toFixed(2);
        return res;
    },

    onChangeAddQuantity(ev) {
        const input = document.querySelector("input[name='add_qty']");
        const depositElem = document.querySelector(".deposit-amount");
        const depositAmt = parseFloat(depositElem.dataset.deposit || 0, 10);
        const qty = parseFloat(input.value || 0, 10);
        const newDepositAmt = depositAmt * qty;
        depositElem.textContent = newDepositAmt.toFixed(2);
        return this._super(...arguments);
    }
});
