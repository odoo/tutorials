import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { _t } from "@web/core/l10n/translation";
import { SignNameAndSignatureDialog } from "@sign/dialogs/dialogs";
import { StampSignDetailsDialog } from "../../dialogs/stamp_dialog";;

patch(SignablePDFIframe.prototype, {
    enableCustom(signItem) {
        super.enableCustom(signItem);
        const signItemElement = signItem.el;
        const signItemData = signItem.data;
        const signItemType = this.signItemTypesById[signItemData.type_id];
        const { name, item_type: type, auto_value: autoValue } = signItemType;
        if (type === _t("stamp")) {
            signItemElement.addEventListener("click", (e) => {
                this.handleSignatureDialogClick(e.currentTarget, signItemType);
            });
        }
    },
    openSignatureDialog(signatureItem, type) {
        if (this.dialogOpen) {
            return;
        }
        const signature = {
            name: this.signerName || "",
            company: this.props.companyInfo?.company || "",
            address: this.props.companyInfo?.address || "",
            city: this.props.companyInfo?.city || "",
            country: this.props.companyInfo?.country || "",
            vat: this.props.companyInfo?.vat || "",
        };
        const frame = {};
        const { height, width } = signatureItem.getBoundingClientRect();
        const signFrame = signatureItem.querySelector(".o_sign_frame");
        this.dialogOpen = true;
        const signatureImage = signatureItem?.dataset?.signature;
        this.closeFn = this.dialog.add(
            type.item_type === "stamp"
                ? StampSignDetailsDialog
                : SignNameAndSignatureDialog,
            {
                frame,
                signature,
                signatureType: type.item_type,
                displaySignatureRatio: width / height,
                activeFrame: Boolean(signFrame) || !type.auto_value,
                mode: "auto",
                defaultFrame: type.frame_value || "",
                hash: this.frameHash,
                signatureImage,
                onConfirm: () => {},
                onConfirmAll: () => {},
            },
            {
                onClose: () => {
                    this.dialogOpen = false;
                },
            }
        );
    }
});
