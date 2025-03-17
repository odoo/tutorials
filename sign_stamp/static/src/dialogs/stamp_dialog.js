import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { SignNameAndSignature, SignNameAndSignatureDialog } from "@sign/dialogs/sign_name_and_signature_dialog";

export class LogoAndStamp extends SignNameAndSignature {
    static template = "sign_stamp.LogoAndStamp";
    static props = {
        ...SignNameAndSignature.props,
    };
}

export class LogoAndStampDialog extends SignNameAndSignatureDialog {
    static props = {
        ...SignNameAndSignatureDialog.props
    };
    static template = "sign_stamp.LogoAndStampDialog";
    static components = {
        Dialog,
        LogoAndStamp,
    };

    get dialogProps() {
        return {
            title: _t("Adopt Your Stamp"),
            size: "md",
        };
    }
}
