import websiteSaleTracking from '@website_sale/js/website_sale_tracking'
import { rpc } from "@web/core/network/rpc";

websiteSaleTracking.include({

    events: Object.assign({
        'click #confirm_btn': '_onConfirmClick',
    }, websiteSaleTracking.prototype.events),

    async _onConfirmClick(ev) {
        ev.preventDefault();
        const checkbox = this.el.querySelector("#want_tax_credit_checkbox");
        if (checkbox && checkbox.checked) {
            const name = this.el.querySelector("#company_name").value.trim();
            const partner_id = this.el.querySelector('input[name="partner_id"]').value;
            const address = JSON.parse(this.el.querySelector("#address").value || '{"error": "Please enter VAT number"}');
            if (address.error) {
                this._displayError(address.error);
                return;
            }
            if (!name) {
                this._displayError("Company name is required.");
                return;
            }
            await rpc('/shop/billing_address/submit', { name, partner_id, address, });
        }
        window.location.href = "/shop/confirm_order";
    },

    _displayError(msg) {
        const errorsDiv = this.el.querySelector("#errors");
        const errorHeader = document.createElement('h5');
        errorHeader.classList.add('text-danger', 'alert', 'alert-danger');
        errorHeader.textContent = msg;
        errorsDiv.replaceChildren(errorHeader);
    },
})
