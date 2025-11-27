import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { getDashboardItems } from "./dashboard_items_service";

export class DashboardConfigurationDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigurationDialog";
    static components = { Dialog };

    setup() {
        const allItems = getDashboardItems();
        const storedConfig = localStorage.getItem("dashboard_configuration");
        const hiddenItems = storedConfig ? JSON.parse(storedConfig) : [];

        this.state = useState({
            items: allItems.map((item) => ({
                ...item,
                hidden: hiddenItems.includes(item.id),
            })),
        });
    }

    onSave() {
        const hiddenItemIds = this.state.items.filter((item) => item.hidden).map((item) => item.id);
        localStorage.setItem("dashboard_configuration", JSON.stringify(hiddenItemIds));
        if (this.props.onConfigChange) {
            this.props.onConfigChange();
        }
        this.props.close();
    }

    onCancel() {
        this.props.close();
    }

    toggleItemVisibility(itemId) {
        const item = this.state.items.find((item) => item.id === itemId);
        if (item) {
            item.hidden = !item.hidden;
        }
    }
}

registry.category("view_dialogs").add("DashboardConfigurationDialog", DashboardConfigurationDialog);
