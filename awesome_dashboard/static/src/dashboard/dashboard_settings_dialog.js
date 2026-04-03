import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };

    setup() {
        const removed = JSON.parse(
            localStorage.getItem("dashboard_removed_items") || "[]"
        );

        this.state = useState({
            items: this.props.items.map(item => ({
                ...item,
                checked: !removed.includes(item.id),
            })),
        });
    }

    toggle(item) {
        item.checked = !item.checked;
    }

    apply() {
        const removedIds = this.state.items
            .filter(i => !i.checked)
            .map(i => i.id);

        localStorage.setItem(
            "dashboard_removed_items",
            JSON.stringify(removedIds)
        );

        this.props.close();
        window.location.reload();
    }
}