/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";
import { PieChart } from "./piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");

        this.state = useState(
            {
                nb_new_orders: 0,
                total_amount: 0,
                average_quantity: 0,
                nb_cancelled_orders: 0,
                average_time: 0,
                orders_by_size: { m: 0, s: 0, xl: 0 },
            });

        onWillStart(async () => {
            try {
                const result = this.statisticsService.data
                this.state.nb_new_orders = result.nb_new_orders;
                this.state.total_amount = result.total_amount;
                this.state.average_quantity = result.average_quantity;
                this.state.nb_cancelled_orders = result.nb_cancelled_orders;
                this.state.average_time = result.average_time;
                this.state.orders_by_size = result.orders_by_size;

                console.log(JSON.stringify(result))

            } catch (error) {
                console.error("Error fetching  statistics:", error);
            }
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
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
