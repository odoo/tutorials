/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };

    setup() {
        const allItems = registry.category("awesome_dashboard_items").getAll();
        const removedIds = JSON.parse(localStorage.getItem("awesome_dashboard.hidden_items") || "[]");

        // Local state with checkboxes
        this.items = useState(
            allItems.map((item) => ({
                ...item,
                visible: !removedIds.includes(item.id),
            }))
        );
    }

    onApply() {
        const hiddenIds = this.items.filter(item => !item.visible).map(item => item.id);
        localStorage.setItem("awesome_dashboard.hidden_items", JSON.stringify(hiddenIds));
        this.props.onClose();  // closes the dialog
        window.location.reload(); // refresh to re-render dashboard with updated state
    }

    onToggleItem(item) {
        item.visible = !item.visible;
    }
}
