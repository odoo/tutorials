import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { _t } from "@web/core/l10n/translation";
import { SignNameAndSignatureDialog } from "@sign/dialogs/dialogs";
import { StampSignDetailsDialog } from "../../dialogs/stamp_dialog";
import { rpc } from "@web/core/network/rpc";

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
        const { signature, signMode, signatureImage } = this._prepareSignatureData(signatureItem, type);
        console.log(signature)
        const frame = {};
        const { height, width } = signatureItem.getBoundingClientRect();
        const signFrame = signatureItem.querySelector(".o_sign_frame");
        this.dialogOpen = true;
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
                mode: signMode,
                defaultFrame: type.frame_value || "",
                hash: this.frameHash,
                signatureImage,
                onConfirm: async () => {
                    this._handleConfirm(signature, frame, signatureItem, type)
                },
                onConfirmAll: async () => {
                    this._handleConfirmAll(signature, frame, type)
                },
            },
            {
                onClose: () => {
                    this.dialogOpen = false;
                },
            }
        );
    },

    _prepareSignatureData(signatureItem, type) {
        const signature = {
            name: this.signerName || "",
            company: this.props.companyInfo?.company || "",
            address: this.props.companyInfo?.address || "",
            city: this.props.companyInfo?.city || "",
            country: this.props.companyInfo?.country || "",
            vat: this.props.companyInfo?.vat || "",
            image: type.auto_value || null,
        };

        const signatureImage = signatureItem?.dataset?.signature;
        const signMode = "auto";
        return { signature, signMode, signatureImage };
    },

    async _handleConfirm(signature, frame, signatureItem, type) {
        if (!signature.isSignatureEmpty && signature.signatureChanged) {
            await this._applySignature(signature, frame, signatureItem, type);
        } else if (signature.signatureChanged) {
            this._resetSignatureItem(signatureItem, type);
        }
        this.closeDialog();
        this.handleInput();
    },

    async _handleConfirmAll(signature, frame, type) {
        this.signerName = signature.name;
        await frame.updateFrame();

        const frameData = frame.getFrameImageSrc();
        const signatureSrc = signature.getSignatureImage();
        type.auto_value = signatureSrc;
        type.frame_value = frameData;

        if (user.userId) {
            await this.updateUserSignature(type);
        }

        await this._fillAllMatchingItems(signatureSrc, frameData, type);
        this.closeDialog();
        this.handleInput();
    },

    async _applySignature(signature, frame, signatureItem, type) {
        this.signerName = signature.name;

        await frame.updateFrame();

        const frameData = frame.getFrameImageSrc();
        const stampImage = signature.getSignatureImage();

        type.auto_value = stampImage;
        type.frame_value = frameData;

        if (user.userId) {
            await this.updateUserSignature(type);
        }
        signatureItem.dataset.signature = stampImage;
        signatureItem.dataset.frame = frameData;

        this.fillItemWithSignature(signatureItem, stampImage, {
            frame: frameData,
            hash: this.frameHash,
        });
    },

    _resetSignatureItem(signatureItem, type) {
        delete signatureItem.dataset.signature;
        delete signatureItem.dataset.frame;
        signatureItem.replaceChildren();

        const signHelperspan = document.createElement("span");
        signHelperspan.classList.add("o_sign_helper");
        signatureItem.append(signHelperspan);

        if (type.placeholder) {
            const placeholderSpan = document.createElement("span");
            placeholderSpan.classList.add("o_placeholder");
            placeholderSpan.innerText = type.placeholder;
            signatureItem.append(placeholderSpan);
        }
    },

    async _fillAllMatchingItems(signatureSrc, frameData, type) {
        for (const page in this.signItems) {
            await Promise.all(
                Object.values(this.signItems[page]).reduce((promises, signItem) => {
                    if (
                        signItem.data.responsible === this.currentRole &&
                        signItem.data.type_id === type.id
                    ) {
                        promises.push(
                            Promise.all([
                                this.adjustSignatureSize(signatureSrc, signItem.el),
                                this.adjustSignatureSize(frameData, signItem.el),
                            ]).then(([data, adjustedFrame]) => {
                                this.fillItemWithSignature(signItem.el, data, {
                                    frame: adjustedFrame,
                                    hash: this.frameHash,
                                });
                            })
                        );
                    }
                    return promises;
                }, [])
            );
        }
    },

    updateUserSignature(type) {
        const signature_type =
            type.item_type === "signature"
                ? "sign_signature"
                : type.item_type === "stamp"
                    ? "stamp_sign_stamp"
                    : "sign_initials";
        return rpc("/sign/update_user_signature", {
            sign_request_id: this.props.requestID,
            role: this.currentRole,
            signature_type: signature_type,
            datas: type.auto_value,
            frame_datas: type.frame_value,
        });
    },
});
