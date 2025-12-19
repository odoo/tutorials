import { App, whenReady } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { Document, SignableDocument } from "@sign/components/sign_request/document_signable";
import { getTemplate } from "@web/core/templates";
import { makeEnv, startServices } from "@web/env";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { _t } from "@web/core/l10n/translation";

patch(Document.prototype,{
    getDataFromHTML(){
        super.getDataFromHTML();
        const { el: parentEl } = this.props.parent;
        this.company = parentEl.querySelector("#o_sign_signer_company_info")?.value;
        this.address = parentEl.querySelector("#o_sign_signer_address_info")?.value;
        this.city = parentEl.querySelector("#o_sign_signer_city_info")?.value;
        this.country = parentEl.querySelector("#o_sign_signer_country_info")?.value;
        this.vat = parentEl.querySelector("#o_sign_signer_vat_info ")?.value;
        this.logo = parentEl.querySelector("#o_sign_signer_logo_info ")?.value;
    },

    get iframeProps(){
        return{
            ...super.iframeProps,
            company : this.company,
            address : this.address,
            city : this.city,
            country : this.country,
            vat : this.vat,
            logo : this.logo,
        }
    },
})

export async function initDocumentToSign(parent) {
    const env = makeEnv();
    await startServices(env);
    await whenReady();
    const app = new App(SignableDocument, {
        name: "Signable Document",
        env,
        props: {
            parent: {el: parent},
            PDFIframeClass: SignablePDFIframe },
        getTemplate,
        dev: env.debug,
        translatableAttributes: ["data-tooltip"],
        translateFn: _t,
    });
    await app.mount(parent.body);
}
