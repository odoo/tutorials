import { patch } from "@web/core/utils/patch";
import { Document } from "@sign/components/sign_request/document_signable";

patch(Document.prototype, {
    getDataFromHTML() {
        super.getDataFromHTML();
        const { el: parentEl } = this.props.parent;
        this.companyInfo = {};
        this.companyInfo.company = parentEl.querySelector("#o_sign_signer_company_input_info")?.value;
        this.companyInfo.address = parentEl.querySelector("#o_sign_signer_address_input_info")?.value;
        this.companyInfo.city = parentEl.querySelector("#o_sign_signer_city_input_info")?.value;
        this.companyInfo.country = parentEl.querySelector("#o_sign_signer_country_input_info")?.value;
        this.companyInfo.vat = parentEl.querySelector("#o_sign_signer_vat_input_info")?.value;
        console.log(this.companyInfo)
    },

    getIframeProps(sign_document_id) {
        const props = super.getIframeProps(sign_document_id);
        const document = this.documents.find((doc) => doc.id === sign_document_id);
        console.log(this.companyInfo)
        return {
            ...props,
            companyInfo: this.companyInfo
        };
    },
});
