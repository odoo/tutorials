/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };

    static props = {
        items: Array,
        onApply: Function,
        close: Function,  // this is automatically passed by Dialog
    };

    setup() {
        const removed = JSON.parse(
            localStorage.getItem("awesome_dashboard.removed_items") || "[]"
        );

        this.state = useState({
            checked: Object.fromEntries(
                this.props.items.map(item => [
                    item.id,
                    !removed.includes(item.id)
                ])
            )
        });
    }

    toggle(itemId) {
        this.state.checked[itemId] = !this.state.checked[itemId];
    }

    apply() {
        const removedIds = Object.entries(this.state.checked)
            .filter(([id, checked]) => !checked)
            .map(([id]) => id);

        localStorage.setItem(
            "awesome_dashboard.removed_items",
            JSON.stringify(removedIds)
        );

        if (this.props.onApply) {
            this.props.onApply();
        }
        this.props.close();
    }
}