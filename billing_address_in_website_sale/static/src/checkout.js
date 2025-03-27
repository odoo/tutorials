import WebsiteSaleCheckout from '@website_sale/js/checkout';
import { rpc } from '@web/core/network/rpc';

WebsiteSaleCheckout.include({

    events: Object.assign({
        'change #want_tax_credit_checkbox': '_onTaxCreditToggle',
        'change #vat_number': '_onChangeVat',
    }, WebsiteSaleCheckout.prototype.events),

    async start() {
        this._onTaxCreditToggle({
            currentTarget: this.el.querySelector('#want_tax_credit_checkbox'),
        });
        return this._super(...arguments);
    },

    async _onTaxCreditToggle(ev) {
        const checkbox = ev.currentTarget;
        const taxContainer = this.el.querySelector('#tax_credit_container');
        taxContainer.classList.toggle('d-none', !checkbox.checked);
        if (!checkbox.checked) {
            const selectedDeliveryAddress = this._getSelectedAddress('delivery');
            await this._selectMatchingBillingAddress(selectedDeliveryAddress.dataset.partnerId);
        }
    },

    async _onChangeVat(ev) {
        const vat = ev.currentTarget.value.trim();
        const address_values = await rpc('/shop/vat/address', { vat: vat });
        if (address_values.error) {
            this.el.querySelector('#vat_warning').textContent = address_values.error;
            this.el.querySelector('#vat_label').textContent = "Vat Number";
            this.el.querySelector('#company_name').value = "";
        }
        else {
            this.el.querySelector('#vat_warning').textContent = "";
            this.el.querySelector('#vat_label').textContent = address_values.country;
            this.el.querySelector('#company_name').value = address_values.name;
        }
        this.el.querySelector('#partner_id').value = "";
    },

});
