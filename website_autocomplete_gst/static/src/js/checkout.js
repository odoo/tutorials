import { rpc } from "@web/core/network/rpc";
import { user } from "@web/core/user";
import publicWidget from '@web/legacy/js/public/public_widget';
import { session } from "@web/session";

publicWidget.registry.WebsiteSaleCheckout.include({
    /**
     * @override
     */
    events: Object.assign({}, publicWidget.registry.WebsiteSaleCheckout.prototype.events, {
        'change #want_tax_credit': '_toggleTaxCreditRow',
    }),

    async start() {
        await this._super.apply(this, arguments);
        this.want_tax_credit_toggle = document.querySelector('#want_tax_credit');
        this.taxCreditContainer = this.el.querySelector('#tax_credit_container');
        this.$vatInput = this.$("#o_vat");
        this.$companyNameInput = this.$("#o_company_name");
        var isSystemUser = await user.hasGroup("base.group_portal");
        if (this.$vatInput.length && (user.isAdmin || isSystemUser || session.is_company)) {
            this.$vatInput.on("change", this._fetchCompanyDetails.bind(this));
        }
        else {
            console.warn("You are not allowed to fetch the details!");
        }
    },

    async _fetchCompanyDetails() {
        const vat = this.$vatInput.val().trim();
        if (!vat) {
            return;
        }
        try {
            const result = await rpc("/shop/get_data", { vat: vat });
            if (result && result.name) {
                console.log(result)
                this.$companyNameInput.val(result.name);
                await this.updateInvoiceAddress('billing', result.vat, result.partner_id);
            } else {
                console.warn("Could not find any company registered to this VAT : ", vat);
            }
        } catch (error) {
            console.error("Failed to fetch company details:", error);
        }
    },

    async _changeAddress(ev) {
        const newAddress = ev.currentTarget;
        if (newAddress.classList.contains('bg-primary')) {
            return;
        }
        const addressType = newAddress.dataset.addressType;
        // Remove the highlighting from the previously selected address card.
        const previousAddress = this._getSelectedAddress(addressType);
        this._tuneDownAddressCard(previousAddress);
        // Highlight the newly selected address card.
        this._highlightAddressCard(newAddress);
        const selectedPartnerId = newAddress.dataset.partnerId;
        await this.updateAddress(addressType, selectedPartnerId);
        // A delivery address is changed.
        if (addressType === 'delivery' || this.taxCreditContainer.dataset.deliveryAddressDisabled) {
            if (this.taxCreditContainer.dataset.deliveryAddressDisabled) {
                // If a delivery address is disabled in the settings, use a billing address as
                // a delivery one.
                await this.updateAddress('delivery', selectedPartnerId);
            }
            if (!this.want_tax_credit_toggle?.checked) {
                await this._selectMatchingBillingAddress(selectedPartnerId);
            }
            // Update the available delivery methods.
            document.getElementById('o_delivery_form').innerHTML = await rpc(
                '/shop/delivery_methods'
            );
            await this._prepareDeliveryMethods();
        }
        this._enableMainButton();  // Try to enable the main button.
    },

    async _toggleTaxCreditRow(ev) {
        const useTaxCredit = ev.target.checked;
        if (!useTaxCredit) {
            this.taxCreditContainer.classList.add('d-none');  // Hide the Tax Credit row.
            const selectedDeliveryAddress = this._getSelectedAddress('delivery');
            await this._selectMatchingBillingAddress(selectedDeliveryAddress.dataset.partnerId);
        } else {
            this._disableMainButton();
            this.taxCreditContainer.classList.remove('d-none');  // Show the Tax Credit row.
        }

        this._enableMainButton();  // Try to enable the main button.
    },

    async updateInvoiceAddress(addressType, vat, partner_id) {
        await rpc('/shop/update_invoice_address', { address_type: addressType, vat: vat || '', partner_id: partner_id || null });
    },

    _isBillingAddressSelected() {
        return this.want_tax_credit_toggle?.checked;
    },
});
