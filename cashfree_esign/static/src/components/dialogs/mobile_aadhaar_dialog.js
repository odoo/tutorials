/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";

export class MobileAadharDialog extends Component {
    static template = "cashfree_esign.MobileAadharDialog";
    static components = { Dialog };

    setup() {
        this.dialog = useService("dialog");
        this.state = useState({ 
            mobile: "", 
            aadhaar: "" 
        });
    }

    submitForm() {
        if (this.state.mobile.length !== 10) {
            alert("Mobile number must be 10 digits.");
            return;
        }
        if (this.state.aadhaar.length !== 4) {
            alert("Aadhaar number must be last 4 digits.");
            return;
        }
        if (this.props.onSubmit) {
            this.props.onSubmit({
                mobile: this.state.mobile,
                aadhaar: this.state.aadhaar
            });
        }
        this.props.close(); 
    }  
}
