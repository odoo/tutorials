import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class SelectSalespersonDialog extends Component {
    static template = "salesperson_pos.SelectSalespersonDialog";
    static props = {
        employees: Array,
        getPayload: Function,
        close: Function,
        title: String,
    };
    static components = { Dialog };

    setup() {
        this.selectSalesperson = this.selectSalesperson.bind(this);
    }

    selectSalesperson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }

    cancelSelection() {
        this.props.getPayload(null);
        this.props.close();
    }
}
