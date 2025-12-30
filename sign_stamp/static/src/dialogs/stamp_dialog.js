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

    onInputStampDetails(ev) {
        const field = ev.target.name;
        if (field === "logo") {
            const file = ev.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                this.props.signature.image = e.target.result;
                this.drawCurrentName();
            };
            reader.readAsDataURL(file);
            return;
        }
        const value = ev.target.value;
        if (field && this.props.signature?.hasOwnProperty(field)) {
            this.props.signature[field] = value;
            this.drawCurrentName();
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
