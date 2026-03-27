import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./piachart/pie_chart";
import { items } from "./db_item";
import { SettingsDialog } from "./settings_dialog/settings_dialog"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.items = useState([]);
        const statistics = useService("awesome_dashboard.statistics");
        this.state = useState(statistics.state);
        this.allItems = registry.category("awesome_dashboard.items").getAll();
        onWillStart(async () => {
            await this.updateItems();
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: "current",
        });
    }
    
    openSettings() {
        const visibleIds = this.items.map(item => item.id);

        const removed = this.allItems
            .filter(item => !visibleIds.includes(item.id))
            .map(item => item.id);

        this.dialog.add(SettingsDialog, {
            items: this.allItems,
            savedRemoved: removed,
            onApply: async (removedIds) => {
                await rpc("/dashboard/save_config", {
                    config: removedIds,
                });
                await this.updateItems();
            },
        });
    }

    async updateItems() {
        const removed = await rpc("/dashboard/get_config");
        const filtered = this.allItems.filter(item => !removed.includes(item.id));

        this.items.splice(0, this.items.length, ...filtered);
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
