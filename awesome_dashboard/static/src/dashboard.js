import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard-item/dashboard-item"
import { NumberCard } from "./number-card/number-card"
import { PieChartCard } from "./pie-chart/pie-chart-card"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));

        // Dashboard items
        this.items = registry.category("awesome_dashboard").getAll();
    }

    actionCustomers() {
        this.action.doAction("base.action_partner_form", { viewType: "kanban" });
    }

    actionLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
