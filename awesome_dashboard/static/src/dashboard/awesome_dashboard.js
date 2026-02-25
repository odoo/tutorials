/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { statisticsStore } from "./services/statistics_service";
import { DashboardItem } from "./dashboard_item";
import { dashboardItemRegistry } from "./dashboard_registry";
import { DashboardSettingsDialog } from "./dashboard_settings_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem };

    static props = {
        onSettingsOpen: Function, // callback to expose settings API
    };

    setup() {
        this.dialog = useService("dialog");
        this.stats = useState(statisticsStore);

        this.allItems = dashboardItemRegistry.getAll();

        // reactive items
        this.state = useState({
            items: this.getFilteredItems(),
        });

        // expose the API
        if (this.props.onSettingsOpen) {
            this.props.onSettingsOpen(() => this.openSettings());
        }
    }

    getFilteredItems() {
        const removed = JSON.parse(
            localStorage.getItem("awesome_dashboard.removed_items") || "[]"
        );
        return this.allItems.filter(item => !removed.includes(item.id));
    }

    openSettings() {
        this.dialog.add(DashboardSettingsDialog, {
            items: this.allItems,
            onApply: () => {
                this.state.items = this.getFilteredItems();
            },
        });
    }
}