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
        signItem.el.addEventListener("click", (ev) => {
            console.log("STAMP CLICKED => opening dialog");
            this.env.services.dialog.add(TestDialog,{
                companyName: this.props.companyInfo.company,
                companyAddress: this.props.companyInfo.address,
                companyCity: this.props.companyInfo.city,
                companyCountry: this.props.companyInfo.country,
                companyVat: this.props.companyInfo.vat
            });
        });
    },
});
