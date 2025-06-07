/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export class SettingDialog extends Component {
    static template = "awesome_dashboard.SettingDialog";
    static components = {
        Dialog,
    };
    static props = {
        close: { type: Function, optional: false },
        onApply: { type: Function, optional: true },
    };

    setup() {
        // Get all dashboard items from the registry
        this.items = registry.category("awesome_dashboard.items").getAll();
        // Read current hidden items from localStorage
        const hiddenItems = JSON.parse(localStorage.getItem("awesome_dashboard_hidden_items")) || [];
        // Create reactive state with a list of items and their "enabled" status
        this.state = useState({
            items: this.items.map(item => ({
                id: item.id,
                description: item.description,
                enabled: !hiddenItems.includes(item.id),
            })),
        });
    }

    applySettings() {
        // Build a list of item IDs for which enabled is false
        const uncheckedItemIds = this.state.items
            .filter(item => !item.enabled)
            .map(item => item.id);
    
        if (this.props.onApply) {
            this.props.onApply(uncheckedItemIds);
        }
        this.props.close();
    }
}
