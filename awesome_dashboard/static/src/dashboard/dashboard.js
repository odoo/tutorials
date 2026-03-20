
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./components/dashboard_item/dashboard_item";
import { PieChart } from "./components/pie_chart/pie_chart";
import { DashboardSettings } from "./components/dashboard_settings/dashboard_settings";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");

        this.statistics = useState(this.statisticsService.statistics);
        const allItems = registry.category("awesome_dashboard.items").getAll();

        const removed = JSON.parse(
            localStorage.getItem("dashboard_removed_items") || "[]"
        );

        this.items = allItems.filter((item) => !removed.includes(item.id));
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
        const allItems = registry.category("awesome_dashboard.items").getAll();
        this.dialog.add(DashboardSettings, {
            items: allItems,
            onApply: (removedIds) => {
                
                localStorage.setItem(
                    "dashboard_removed_items",
                    JSON.stringify(removedIds)
                );
                window.location.reload();
            },
        });
    }
}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);