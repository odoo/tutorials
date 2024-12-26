/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";


export class DashboardDialog extends Component {
    static template = "awesome_dashboard.DashboardDialog";
    static components = { Dialog, CheckBox };
    static props = {
        close: { type: Function },
        items: { type: Array },
        inactive_items: { type: Array },
        updateInactiveItems: { type: Function }
    };

    setup() {
        this.items = useState([]);
        this.props.items.forEach(item => {
            let active_item = {
                ...item,
                is_active: !this.props.inactive_items.includes(item.id)
            }
            this.items.push(active_item);
        });
    }

    onChecked(checked, item) {
        item.is_active = checked;
    }

    close_dialog() {
        this.props.close();
        this.props.updateInactiveItems(
            this.items.filter((item) => !item.is_active).map((item) => item.id)
        )
    }
}
