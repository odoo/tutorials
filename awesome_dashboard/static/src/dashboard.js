/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboarditem/dashboarditem";
import { PieChart } from "./components/piechart/piechart";
import {rpc} from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout,  PieChart, DashboardItem}
    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);
        this.actionService = useService("action");
        this.stats = useState({
            newOrders: 0,
            totalAmount: 0.0,
            avgTShirtsPerOrder: 0.0,
            cancelledOrders: 0,
            avgProcessingTime: 0,
        });

        onWillStart(async () => {
            const data = await rpc("/awesome_dashboard/statistics", {});
                this.stats.newOrders = data.nb_new_orders;
                this.stats.totalAmount = data.total_amount;
                this.stats.avgTShirtsPerOrder = data.average_quantity;
                this.stats.cancelledOrders = data.nb_cancelled_orders;
                this.stats.avgProcessingTime = data.average_time;
         });
    }
    openCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }
    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "current",
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
