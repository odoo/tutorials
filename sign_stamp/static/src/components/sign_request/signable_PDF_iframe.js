import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { TestDialog } from "../../dialogs/test_dialog";

patch(SignablePDFIframe.prototype, {
    enableCustom(signItem) {
        super.enableCustom(signItem);
        const signItemType = this.signItemTypesById[signItem.data.type_id];
        if (signItemType.item_type !== "stamp") {
            return;
        }

        signItem.el.value = `
            ${this.props.companyInfo.company}
            ${this.props.companyInfo.address}
            ${this.props.companyInfo.city}
            ${this.props.companyInfo.country}
            ${this.props.companyInfo.vat}
        `

        signItem.el.addEventListener("click", (ev) => {
            console.log("STAMP CLICKED => opening dialog");
            this.env.services.dialog.add(TestDialog, {
                companyName: this.props.companyInfo.company,
                companyAddress: this.props.companyInfo.address,
                companyCity: this.props.companyInfo.city,
                companyCountry: this.props.companyInfo.country,
                companyVat: this.props.companyInfo.vat,
                signItemEl: signItem.el,
                onCancel() {
                    this.props.close();
                },
                OnSign() {
                    const companyNameInput = document.querySelector('#company_name_input')?.value || ""
                    const companyAddressInput = document.querySelector('#company_address_input')?.value || "" 
                    const companyCityInput = document.querySelector('#company_city_input')?.value || "" 
                    const companyCountryInput = document.querySelector('#company_country_input')?.value || "" 
                    const companyVatInput = document.querySelector('#company_vat_input')?.value || ""
                    this.companyName = companyNameInput 
                    this.companyAddress = companyAddressInput 
                    this.companyCity = companyCityInput 
                    this.companyCountry = companyCountryInput 
                    this.companyVat = companyVatInput 
                    signItem.el.value = `
                        ${this.companyName}
                        ${this.companyAddress}
                        ${this.companyCity}
                        ${this.companyCountry}
                        ${this.companyVat}
                    ` 
                    this.props.close();
                },
            });
        });
    },
});
