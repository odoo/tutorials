/** @odoo-module */

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class QuantityDialog extends Component {
    static template = 'pos_product_uom.QuantityDialog';
    static components = { Dialog };

    setup() {
        this.notification = useService('notification');
    }

    confirmAction() {
        if (this.props.quantity == '') {
            this.notification.add(_t("Oops! Numbers first, please! Let's try that again. 😊"), {
                type: 'info'
            })
            return
        }
        this.props.onConfirm(this.props.quantity);
        this.props.close(); 
    }

    discardAction() {
        this.props.close();
    }
}
