/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.statsService = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            this.stats = await this.statsService.loadStatistics();
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            name: "Leads",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry
    .category("actions")
    .add("awesome_dashboard.dashboard", AwesomeDashboard);
