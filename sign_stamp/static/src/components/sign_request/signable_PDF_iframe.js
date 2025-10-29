import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";
import { SignNameAndSignatureDialog } from "@sign/dialogs/dialogs";
import { StampSignDetailsDialog } from "../../dialogs/stamp_sign_add_stamp_dialog";

patch(SignablePDFIframe.prototype, {
  enableCustom(signItem) {
    super.enableCustom(signItem);

    const signItemElement = signItem.el;
    const signItemData = signItem.data;
    const signItemType = this.signItemTypesById[signItemData.type_id];
    const { item_type: type } = signItemType;

    if (type === _t("stamp")) {
      signItemElement.addEventListener("click", (e) => {
        this.handleSignatureDialogClick(e.currentTarget, signItemType);
      });
    }
  },

  openSignatureDialog(signatureItem, type) {
    if (this.dialogOpen) return;

    const { signature, signMode, signatureImage } = this._prepareSignatureData(
      signatureItem,
      type
    );
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
        onConfirm: () =>
          this._handleConfirm(signature, frame, signatureItem, type),
        onConfirmAll: () => this._handleConfirmAll(signature, frame, type),
        onCancel: () => this.closeDialog(),
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
      name: this.props.signerName,
      company: this.props.company,
      address: this.props.address,
      city: this.props.city,
      country: this.props.country,
      vat: this.props.vat,
      logo: this.props.logo,
    };

    const signatureImage = signatureItem?.dataset?.signature;
    const signMode = type.auto_value ? "auto" : "draw";

    if (signMode === "draw" && signatureImage) {
      signature.signatureImage = signatureImage;
    }

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
    return rpc("/sign/update_user_signature", {
      sign_request_id: this.props.requestID,
      role: this.currentRole,
      signature_type:
        type.item_type === "signature"
          ? "sign_signature"
          : type.item_type === "stamp"
          ? "stamp_sign"
          : "sign_initials",
      datas: type.auto_value,
      frame_datas: type.frame_value,
    });
  },

  getSignatureValueFromElement(item) {
    const customTypes = {
      stamp: () => item.el.dataset.signature,
    };
    const type = item.data.type;
    return type in customTypes
      ? customTypes[type]()
      : super.getSignatureValueFromElement(item);
  },
});
