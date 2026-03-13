import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboard_item";
import { DashboardSettingsDialog } from "./settings_dialog";

class AwesomeDashboard extends Component {
    static components = {
        Layout,
        DashboardItem,
        DashboardSettingsDialog,
    };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");

        this.state = useState({
            stats: this.statistics.state,
            items: [],
        });

        this.loadItems();
    }

    loadItems() {
        const allItems = registry.category("awesome_dashboard.items").getAll();

        const stored = JSON.parse(
            localStorage.getItem("awesome_dashboard.removed_items") || "[]",
        );

        this.state.items = allItems.filter(
            (item) => !stored.includes(String(item.id)),
        );
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "dashboard",
            target: "new",
            res_model: "crm.lead",
            views: [[false, "list"]],
        });
    }
    openSettings = () => {
        const allItems = registry.category("awesome_dashboard.items").getAll();

        this.dialog.add(DashboardSettingsDialog, {
            title: "Settings",
            items: allItems,
            onApply: () => this.loadItems(),
        });
    };
}

registry
    .category("lazy_components")
    .add("awesome_dashboard.dashboard", AwesomeDashboard);
