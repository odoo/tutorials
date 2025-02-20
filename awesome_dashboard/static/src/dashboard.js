import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./components/pie_chart/pie_chart";
import { Component, onWillStart } from "@odoo/owl";

import { DashboardItem } from "./components/dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";
    
    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");

        this.statistics = {
            average_quantity: 0,
            average_time: 0,
            nb_cancelled_orders: 0,
            nb_new_orders: 0,
            orders_by_size: {
                'm': 0,
                's': 0,
                'xl': 0,
            },
            total_amount: 0,
        };

        onWillStart(async () => {
            this.statistics = await this.statisticsService.loadStatistics();
        })
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, 'list'], [false, 'form']],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
