/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statisticsService");
        this.state = useState({
            response: {
                average_quantity: 0,
                average_time: 0,
                nb_cancelled_orders: 0,
                nb_new_orders: 0,
                total_amount: 0,
                orders_by_size: {
                    m: 0,
                    s: 0,
                    xl: 0
                },
            }
        });

        onWillStart(async () => {
            const response = await this.statisticsService.loadStatistics();
            this.state.response = {
                average_quantity: response.average_quantity,
                average_time: response.average_time,
                nb_cancelled_orders: response.nb_cancelled_orders,
                nb_new_orders: response.nb_new_orders,
                total_amount: response.total_amount,
                orders_by_size: response.orders_by_size
            };
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
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
