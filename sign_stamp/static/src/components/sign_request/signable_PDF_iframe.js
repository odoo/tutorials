import { LogoAndStampDialog } from "../../dialogs/stamp_dialog";
import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { startSignItemNavigator } from "./sign_item_navigator";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { SignNameAndSignatureDialog } from "@sign/dialogs/dialogs";
import { user } from "@web/core/user";
import { _t } from "@web/core/l10n/translation";


patch(SignablePDFIframe.prototype, {

    enableCustom(signItem) {
        super.enableCustom(signItem);
        const signItemElement = signItem.el;
        const signItemData = signItem.data;
        const signItemType = this.signItemTypesById[signItemData.type_id];
        if(signItemType.item_type === 'stamp'){
            signItemElement.addEventListener("click", (e) => {
                this.handleSignatureDialogClick(e.currentTarget, signItemType);
            });
        }
    },

    openSignatureDialog(signatureItem, type){
        if (this.dialogOpen) {
            return;
        }
        const signature = {
            name : this.props.signerName,
            company: this.props.company,
            address: this.props.address,
            city : this.props.city,
            country: this.props.country,
            vat: this.props.vat,
            logo: this.props.logo,
        };
        this.dialogOpen = true;
        // If we already have an image, we propagate it to populate the "draw" tab
        const signatureImage = signatureItem?.dataset?.signature;
        if (signatureImage) {
            signature.signatureImage = signatureImage;
        }
        if(type.item_type === 'stamp'){
            this.closeFn = this.dialog.add(
                LogoAndStampDialog,
                this.dialogData(signatureItem,type),
                {
                    onClose: () => {
                        this.dialogOpen = false;
                    },
                }
            );
        }
        else{
            this.closeFn = this.dialog.add(
                SignNameAndSignatureDialog,
                this.dialogData(signatureItem,type),
                {
                    onClose: () => {
                        this.dialogOpen = false;
                    },
                }
            );
        }
    },

    dialogData(signatureItem, type){
        const signature = {
            name : this.props.signerName,
            company: this.props.company,
            address: this.props.address,
            city : this.props.city,
            country: this.props.country,
            vat: this.props.vat,
            logo: this.props.logo
        };
        const frame = {};
        const { height, width } = signatureItem.getBoundingClientRect();
        const signFrame = signatureItem.querySelector(".o_sign_frame");
        const signMode = type.auto_value ? "draw" : "auto"
        const signatureImage = signatureItem?.dataset?.signature;
        if (signatureImage) {
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
                    type.auto_value = signatureSrc;
                    type.frame_value = frameData;
                    if (user.userId) {
                        await this.updateUserSignature(type);
                    }
                    this.fillItemWithSignature(signatureItem, signatureSrc, {
                        frame: frameData,
                        hash: this.frameHash,
                    });
                } else if (signature.signatureChanged) {
                    // resets the sign item
                    delete signatureItem.dataset.signature;
                    delete signatureItem.dataset.frame;
                    signatureItem.replaceChildren();
                    const signHelperSpan = document.createElement("span");
                    signHelperSpan.classList.add("o_sign_helper");
                    signatureItem.append(signHelperSpan);
                    if (type.placeholder) {
                        const placeholderSpan = document.createElement("span");
                        placeholderSpan.classList.add("o_placeholder");
                        placeholderSpan.innerText = type.placeholder;
                        signatureItem.append(placeholderSpan);
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
                        Object.values(this.signItems[page]).reduce((promiseList, signItem) => {
                            if (
                                signItem.data.responsible === this.currentRole &&
                                signItem.data.type_id === type.id
                            ) {
                                promiseList.push(
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
                            return promiseList;
                        }, [])
                    );
                }
                this.closeDialog();
                this.handleInput();
            },
            onCancel: () => {
                this.closeDialog();
            },
        }
    },

    updateUserSignature(type) {
        return rpc("/sign/update_user_signature", {
            sign_request_id: this.props.requestID,
            role: this.currentRole,
            signature_type: type.item_type === "signature" ? "sign_signature" :
                            type.item_type === "stamp" ? "sign_stamp" :
                            "sign_initials",
            datas: type.auto_value,
            frame_datas: type.frame_value,
        });
    },

    getSignatureValueFromElement(item) {
        if(item.data.type === "stamp"){
            return item.el.dataset.signature;
        }
        else{
            return super.getSignatureValueFromElement(item);
        }
    },

    postRender() {
        const refreshSignItemsIntervalId = setInterval(() => this.refreshSignItems(), 1000);
        this.cleanupFns.push(() => clearInterval(refreshSignItemsIntervalId));
        if (this.readonly) {
            return;
        }
        this.navigator = startSignItemNavigator(
            this,
            this.root.querySelector("#viewerContainer"),
            this.signItemTypesById,
            this.env
        );
        this.checkSignItemsCompletion();

        this.root.querySelector("#viewerContainer").addEventListener("scroll", () => {
            if (!this.navigator.state.isScrolling && this.navigator.state.started) {
                this.navigator.setTip(_t("next"));
            }
        });

        this.root.querySelector("#viewerContainer").addEventListener("keydown", (e) => {
            if (e.key !== "Enter" || (e.target.tagName.toLowerCase() === 'textarea')) {
                return;
            }
            this.navigator.goToNextSignItem();
        });

        this.props.validateBanner
            .querySelector(".o_validate_button")
            .addEventListener("click", () => {
                this.signDocument();
        });
    }

});
