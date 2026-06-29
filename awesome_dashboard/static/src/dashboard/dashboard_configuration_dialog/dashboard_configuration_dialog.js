import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardConfigurationDialog extends Component {
    static template =
        "awesome_dashboard.DashboardConfigurationDialog";

    static components = {
        Dialog,
    };

    static props = {
        close: Function,
        items: Array,
    };

    setup() {
        const removedItems = JSON.parse(
            localStorage.getItem(
                "awesome_dashboard_removed_items"
            ) || "[]"
        );

        this.state = useState({
            items: this.props.items.map(item => ({
                ...item,
                checked: !removedItems.includes(item.id),
            })),
        });
    }

    apply() {
        const removedItems = this.state.items
            .filter(item => !item.checked)
            .map(item => item.id);

        localStorage.setItem(
            "awesome_dashboard_removed_items",
            JSON.stringify(removedItems)
        );

        this.props.close();

        window.location.reload();
    }
}
