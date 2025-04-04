import WebsiteSaleCheckout from '@website_sale/js/checkout';
import { rpc } from '@web/core/network/rpc';

WebsiteSaleCheckout.include({

    events: Object.assign({
        'change #want_tax_credit_checkbox': '_onTaxCreditToggle',
        'change #vat_number': '_onChangeVat',
    }, WebsiteSaleCheckout.prototype.events),

    async start() {
        this.vatLable = this.el.querySelector('#vat_label');
        this.companyName = this.el.querySelector('#company_name');
        this.address = this.el.querySelector('#address');
        this.partnerId = this.el.querySelector('#partner_id');
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
        const addressValues = await rpc('/shop/vat/address', { vat });
        this.vatLable.textContent = addressValues.country_id ? addressValues.country_id.display_name : "Vat Number";
        this.companyName.value = addressValues.name || "";
        this.address.value = JSON.stringify(addressValues);
        this.partnerId.value = "";
    },

});
