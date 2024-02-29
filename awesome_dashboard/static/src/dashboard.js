/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./Dashboard_item/Dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.statistics = useService("awesome_dashboard.statistics");

        this.state = useState({ statistics: {}, shirt_sizes: {} });

        onWillStart(async () => {
            this.updateStatistics(await this.statistics.loadStatistics());
        });


    }

    updateStatistics(new_statistics) {
        this.state.statistics = new_statistics
        this.state.shirt_sizes = {
            labels: Object.keys(new_statistics.orders_by_size),
            datasets: [{
                data: Object.values(new_statistics.orders_by_size),
            }]
        };
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
