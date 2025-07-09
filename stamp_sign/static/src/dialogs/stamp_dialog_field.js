import { SignNameAndSignature } from "@sign/dialogs/sign_name_and_signature_dialog";

export class Stamp extends SignNameAndSignature {
    static template = "stamp_sign.Stamp";

    static props = {
        ...SignNameAndSignature.props,
        noInputName: Boolean,
    };

    triggerFileUpload() {
        const fileInput = document.querySelector("input[name='logo']");
        if (fileInput) {
            fileInput.click();
        }
    }

    onInputSignName(ev) {
        this.props.signature.name = ev.target.value;
        this.props.signature = { ...this.props.signature, name: ev.target.value };
        this.render();
    }

    onInputData(ev) {
        const fieldName = ev.target.name;
        const value = ev.target.value;
        this.props.signature[fieldName] = value;
        this.props.signature = { ...this.props.signature, [fieldName]: value };
        this.render();
    }
}
