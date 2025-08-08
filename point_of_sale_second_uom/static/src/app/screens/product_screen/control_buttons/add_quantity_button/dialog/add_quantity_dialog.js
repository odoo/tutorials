import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";


export class AddQuantityDialog extends Component {
    static template = "pos.AddQuantityDialog";
    static components = {
        Dialog,
    };
    static props = {
        confirm: Function,
        close: Function,
        second_uom: {type: String, optional: true},
        quantity: {type: Number},
    };
    get quantity1() {
        return this.props.quantity;
    }
    confirm() {
        this.props.confirm(this.quantity1);
        this.props.close();
    }
}
