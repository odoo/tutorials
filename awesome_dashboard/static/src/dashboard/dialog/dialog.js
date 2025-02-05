/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { dashboardRegistry } from "../dashboarditem/dashboard_items";

export class SettingsDialog extends Component {

    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };
    setup() {
        this.dialogService = useService("dialog");
        this.items = Object.values(dashboardRegistry.getAll());

        const savedHiddenItems = JSON.parse(localStorage.getItem("hidden_dashboard_items"));
        this.state = useState({
            hiddenItems: new Set(savedHiddenItems),
        });
    }

    toggleItem(event) {
        if (this.state.hiddenItems.has(event.target.id)) {
            this.state.hiddenItems.delete(event.target.id);
        } else {
            this.state.hiddenItems.add(event.target.id);
        }
    }

    applySettings() {
        localStorage.setItem("hidden_dashboard_items", JSON.stringify([...this.state.hiddenItems]));
        this.props.onApply([...this.state.hiddenItems]);

        this.dialogService.closeAll();
    }
}

