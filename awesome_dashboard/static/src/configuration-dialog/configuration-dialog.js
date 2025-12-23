import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.configuration-dialog";
    static props = {
        items: { type: Array, element: Object },
        disabledItems: { type: Array, element: String },
        updateConfiguration: Function,
        close: { type: Function, optional: true },
    };
    static components = { Dialog };

    setup() {
        this.items = this.props.items.map((item) => ({
            ...item,
            disabled: this.props.disabledItems.includes(item.id),
        }));
    }

    toggleMasked(item) {
        item.disabled = !item.disabled;
    }

    applyConfigurationChanges() {
        const disabledItems = this.items.filter((item) => item.disabled).map((item) => item.id);
        this.props.updateConfiguration(disabledItems);
        if(this.props.close) {
            this.props.close();
        }
    }
}
