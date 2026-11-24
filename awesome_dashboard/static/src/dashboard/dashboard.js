
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboardItem";
import { PieChart } from "./pie_chart/pie_chart";
import "./dashboard_items";

console.log("dashboard.js loaded");

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboardView";

    static components = {
        Layout,
        DashboardItem,
        PieChart,
    };

    setup() {
        this.action = useService("action");

        const statisticsService = useService(
            "awesome_dashboard.statistics"
        );

        this.statistics = useState(statisticsService);
        this.items = registry.category("awesome_dashboard").getAll();
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLead() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("lazy_components").add(
    "AwesomeDashboard",
    AwesomeDashboard
);
