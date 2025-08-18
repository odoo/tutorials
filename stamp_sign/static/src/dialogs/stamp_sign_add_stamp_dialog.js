import { Dialog } from "@web/core/dialog/dialog";
import { SignNameAndSignature, SignNameAndSignatureDialog } from "@sign/dialogs/sign_name_and_signature_dialog";

export class StampSignDetails extends SignNameAndSignature {
    static template = "stamp_sign.StampSignDetails";

    triggerFileUpload() {
        const fileInput = document.querySelector("input[name='logo']");
        if (fileInput) {
            fileInput.click();
        }
    }
}

export class StampSignDetailsDialog extends SignNameAndSignatureDialog {
    static template = "stamp_sign.StampSignDetailsDialog";

    static components = { Dialog, StampSignDetails };

    get dialogProps() {
        return {
            title: "Adopt Your Stamp",
        };
    }
}
