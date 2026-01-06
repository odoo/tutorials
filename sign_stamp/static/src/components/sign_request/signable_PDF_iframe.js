import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { SignNameAndSignatureDialog } from "@sign/dialogs/dialogs";
import { StampSignDetailsDialog } from "../../dialogs/stamp_dialog";

patch(SignablePDFIframe.prototype, {
    enableCustom(signItem) {
        super.enableCustom(signItem);
        const signItemType = this.signItemTypesById[signItem.data.type_id];
        if (!signItemType || signItemType.item_type !== "stamp") {
            return;
        }
        signItem.el.addEventListener("click", (e) => {
            this.openSignatureDialog(e.currentTarget, signItemType);
        });
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
        this.closeFn = this.dialog.add(
            type.item_type === "stamp" ? StampSignDetailsDialog : SignNameAndSignatureDialog,
            {
                frame,
                signature,
                signatureType: type.item_type,
                displaySignatureRatio: width / height,
                activeFrame: Boolean(signFrame) || !type.auto_value,
                mode: "auto",
                defaultFrame: type.frame_value || "",
                hash: this.frameHash,
                onConfirm: async () => {
                    if (!signature.isSignatureEmpty && signature.signatureChanged) {
                        const signatureName = signature.name;
                        this.props.updateSignerName(signatureName);
                        await frame.updateFrame();
                        const frameData = frame.getFrameImageSrc();
                        const signatureSrc = signature.getSignatureImage();
                        this.fillItemWithSignature(signatureItem, signatureSrc, {
                            frame: frameData,
                            hash: this.frameHash,
                        });
                    } 
                    this.closeDialog();
                    this.handleInput();
                },
            },
            {
                onClose: () => {
                    this.dialogOpen = false;
                },
            }
        );
    },

    getSignatureValueFromElement(item) {
        return item.data.type === "stamp" ? item.el.dataset.signature : super.getSignatureValueFromElement(item)
    },
});
