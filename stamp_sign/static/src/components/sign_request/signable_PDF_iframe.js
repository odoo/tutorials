/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";

patch(SignablePDFIframe.prototype, {

    enableCustom(signItem) {
        super.enableCustom(signItem);

        const signItemElement = signItem.el;
        const signItemData = signItem.data;
        const signItemType = this.signItemTypesById[signItemData.type_id];
        const { item_type: type } = signItemType;

        if (type === "stamp") {
            signItemElement.addEventListener("click", (e) => {
                this.handleSignatureDialogClick(e.currentTarget, signItemType);
            });
        }
    },
});
