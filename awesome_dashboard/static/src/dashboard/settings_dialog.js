import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";

    static props = {
        title: { type: String, optional: true },
        items: { type: Array, optional: true },
        close: Function,
        onApply: { type: Function, optional: true },
    };

    static components = { Dialog };

    setup() {
        const allItems =
            this.props.items ||
            registry.category("awesome_dashboard.items").getAll();

        const stored = JSON.parse(
            localStorage.getItem("awesome_dashboard.removed_items") || "[]",
        );

        const removedMap = {};
        for (const id of stored) {
            removedMap[String(id)] = true;
        }

        this.state = useState({
            items: allItems,
            removedItems: removedMap,
        });
    }

    toggle = (item) => {
        const key = String(item.id);

        if (this.state.removedItems[key]) {
            delete this.state.removedItems[key];
        } else {
            this.state.removedItems[key] = true;
        }
    };

    isChecked(item) {
        return !this.state.removedItems[String(item.id)];
    }

    apply() {
        const removedIds = Object.keys(this.state.removedItems);

        localStorage.setItem(
            "awesome_dashboard.removed_items",
            JSON.stringify(removedIds),
        );

        if (this.props.onApply) {
            this.props.onApply();
        }

        this.props.close();
    }
}
