import websiteSaleTracking from '@website_sale/js/website_sale_tracking'
import { rpc } from "@web/core/network/rpc";

websiteSaleTracking.include({
    events: Object.assign({
        'click #confirm_btn': '_onConfirmClick',
    }, websiteSaleTracking.prototype.events),

    async _onConfirmClick() {
        const checkbox = this.el.querySelector("#want_tax_credit_checkbox");
        if (checkbox.checked) {
            const vat = this.el.querySelector("#vat_number").value.trim();
            const companyName = this.el.querySelector("#company_name").value.trim();
            const warning = document.querySelector('#vat_warning');
            const partnerId = this.el.querySelector('input[name="partner_id"]').value;
            if (!vat) {
                warning.textContent = "VAT number is required.";
                return;
            }
            const data = { vat, name: companyName };
            if (partnerId) data.partner_id = partnerId;
            const response = await rpc('/shop/billing_address/submit', data);
            if (response.error) {
                warning.textContent = response.error;
                return;
            }
        }
        window.location.href = "/shop/confirm_order";
    }
})
