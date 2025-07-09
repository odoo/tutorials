import { user } from "@web/core/user";
import { _t } from "@web/core/l10n/translation";
import { StampDialog } from "../../dialogs/stamp_add_dialog";
import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { SignNameAndSignatureDialog } from "@sign/dialogs/dialogs"


patch(SignablePDFIframe.prototype, {
    enableCustom(signItem) {
        super.enableCustom(signItem);

        const signItemElement = signItem.el;
        const signItemData = signItem.data;
        const signItemType = this.signItemTypesById[signItemData.type_id];

        if (signItemType.item_type === 'stamp') {
            signItemElement.addEventListener("click", (e) => {
                this.handleSignatureDialogClick(e.currentTarget, signItemType);
            });
        }
    },

    openSignatureDialog(signatureItem, type) {
        if (this.dialogOpen) {
            return;
        }

        this.dialogOpen = true;

        const dataRequired = this.stampDetailsInDialog(signatureItem, type);

        this.closeFn = this.dialog.add(
            type.item_type === "stamp" ? StampDialog : SignNameAndSignatureDialog,
            dataRequired,
            {
                onClose: () => {
                    this.dialogOpen = false;
                },
            }
        );
    },

    stampDetailsInDialog(signatureItem, type) {
        const signature = {
            name: this.props.signerName,
            company: this.props.company,
            address: this.props.address,
            city: this.props.city,
            country: this.props.country,
            vat: this.props.vat,
            logo: this.props.logo,
        }

        const frame = {};
        const { height, width } = signatureItem.getBoundingClientRect();
        const signFrame = signatureItem.querySelector(".o_sign_frame");
        const signatureImage = signatureItem?.dataset?.signature;
        const signMode = type.auto_value ? "draw" : "auto"
        if (signMode == "draw" && signatureImage) {
            signature.signatureImage = signatureImage;
        }

        return {
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
                if (!signature.isSignatureEmpty && signature.signatureChanged) {
                    const signatureName = signature.name;
                    this.signerName = signatureName;
                    await frame.updateFrame();
                    const frameData = frame.getFrameImageSrc();
                    const signatureSrc = signature.getSignatureImage();
                    type.auto_value = frameData;
                    type.frame_value = frameData;
                    if (user.userId) {
                        await this.updateUserSignature(type);
                    }
                    this.fillItemWithSignature(signatureItem, signatureSrc, {
                        frame: frameData,
                        hash: this.frameHash,
                    });
                } else if (signature.signatureChanged) {
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
                        signatureItem.append(placeholderSpan)
                    }
                }
                this.closeDialog();
                this.handleInput();
            },
            onConfirmAll: async () => {
                const signatureName = signature.name;
                this.signerName = signatureName;
                await frame.updateFrame();
                const frameData = frame.getFrameImageSrc();
                const signatureSrc = signature.getSignatureImage();
                type.auto_value = signatureSrc;
                type.frame_value = frameData;
                if (user.userId) {
                    await this.updateUserSignature(type);
                }
                for (const page in this.signItems) {
                    await Promise.all(
                        Object.values(this.signItems[page]).reduce((promishList, signItem) => {
                            if (
                                signItem.data.responsible === this.currentRole &&
                                signItem.data.type_id === type.id
                            ) {
                                promishList.push(
                                    Promise.all([
                                        this.adjustSignatureSize(signatureSrc, signItem.el),
                                        this.adjustSignatureSize(frameData, signItem.el),
                                    ]).then(([data, frameData]) => {
                                        this.fillItemWithSignature(signItem.el, data, {
                                            frame: frameData,
                                            hash: this.frameHash,
                                        });
                                    })
                                );
                            }
                            return promishList;
                        }, [])
                    );
                }
                this.closeDialog();
                this.handleInput();
            },
            onCancel: () => {
                this.closeDialog();
            },
        };
    },

    getSignatureValueFromElement(item) {
        if (item.data.type === "stamp") {
            return item.el.dataset.signature;
        }
        else {
            return super.getSignatureValueFromElement(item);
        }
    },

});
