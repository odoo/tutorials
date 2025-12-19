import { Dialog } from "@web/core/dialog/dialog";
import { SignNameAndSignature, SignNameAndSignatureDialog } from "@sign/dialogs/sign_name_and_signature_dialog";

export class Stamp extends SignNameAndSignature {
    debugger;
    static template = "sign_stamp.Stamp";
    static props = {
        ...SignNameAndSignature.props,
    };
    triggerFileUpload() {
        const fileInput = document.querySelector("input[name='logo']");
        if (fileInput) {
            fileInput.click();
        } else {
            console.error("File input not found!");
        }
        }
}

export class StampDialog extends SignNameAndSignatureDialog {
    static props = {
        ...SignNameAndSignatureDialog.props
    };
    static template = "sign_stamp.StampDialog";
    static components = {
        Dialog,
        Stamp,
    };
    get dialogPropsStamp() {
        return {
            title: "Adopt Your Stamp",
            size: "md",
        };
    }
}
