/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";   

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart};

    setup() {
        this.actionService = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);
        const dashboardItemsRegistry = registry.category("awesome_dashboard");
        this.items = dashboardItemsRegistry.getAll();
    }

    openCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }

    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);