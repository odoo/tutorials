/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.stats_service = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            this.stats = await this.stats_service.load();
            this.shirts_data = {
                labels: Object.keys(this.stats.orders_by_size),
                datasets: [{
                    data: Object.values(this.stats.orders_by_size),
                }]
            };
        });
    }

    showCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "tree"],
                [false, "form"],
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
