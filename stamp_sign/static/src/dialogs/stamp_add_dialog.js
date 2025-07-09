import { Dialog } from "@web/core/dialog/dialog";
import { SignNameAndSignatureDialog } from "@sign/dialogs/sign_name_and_signature_dialog";
import { Stamp } from "./stamp_dialog_field";

export class StampDialog extends SignNameAndSignatureDialog {
    static template = "stamp_sign.StampDialog";

    static components = { Dialog, Stamp };

}
