import { patch } from "@web/core/utils/patch";
import { Document } from "@sign/components/sign_request/document_signable";


patch(Document.prototype, {
    getDataFromHTML() {
        super.getDataFromHTML()
        const { el: parentEl } = this.props.parent;

        this.company = parentEl.querySelector("company_input")?.value;
        this.address = parentEl.querySelector("address_input")?.value;
        this.city = parentEl.querySelector("city_input")?.value;
        this.country = parentEl.querySelector("country_input")?.value;
        this.vat = parentEl.querySelector("vat_input")?.value;
        this.logo = parentEl.querySelector("logo_input")?.value;
    },
    get iframeProps() {
        return {
            ...super.iframeProps,
            company: this.company,
            address: this.address,
            city: this.city,
            country: this.country,
            vat: this.vat,
            logo: this.logo,
        }
    },
})
