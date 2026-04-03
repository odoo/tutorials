import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

import { DashboardItem } from "./components/dashboard_item/dashboard_item";
import { PieChart } from "./components/pie_chart/pie_chart";
import { DashboardSettings } from "./components/dashboard_settings/dashboard_settings";
import "./dashboard_items";
import { _t } from "@web/core/l10n/translation";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");

        this.statistics = useState(this.statisticsService.state);
        this.removed = useState({ ids: [] });
        this.allItems = registry.category("awesome_dashboard.items").getAll();
        this.items = useState([]);
        console.log("ITEMS:", this.items);
        console.log("All items:", this.allItems);
        console.log("Dashboard items:", this.items);

        onWillStart(async () => {
            try {
                const config = await rpc("/awesome_dashboard/get_config");

                this.removed.ids = JSON.parse(config || "[]");

                this._computeItems();

                await this.statisticsService.loadStatistics();

            } catch (e) {
                console.error("Failed to load dashboard config:", e);
                this.removed.ids = [];
                this._computeItems();
            }
        });
    }

    _computeItems() {
        this.items.splice(0);

        const filtered = this.allItems.filter(
            (item) => !this.removed.ids.includes(item.id)
        );

        this.items.push(...filtered);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openSettings() {
        this.dialog.add(DashboardSettings, {
            items: this.allItems,
            removed: [...this.removed.ids],
            onApply: async (removedIds) => {
                await rpc("/awesome_dashboard/save_config", {
                    config: JSON.stringify(removedIds),
                });
                this.removed.ids = removedIds;
                this._computeItems();
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
