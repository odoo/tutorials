/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService, } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboardItem";
import { PieChart } from "./components/PieChart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {

        this.action = useService("action")
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);
        // this.statistics = useState({
        //     new_orders: 0,
        //     total_sales: 0,
        //     avgerage_quantity: 0,
        //     cancelled_orders: 0,
        //     avg_order_time: 0,
        //     orders_by_size: {  m: 0, s: 0, xl: 0, },
        // });


        onWillStart(async () => {
            await this.statisticsService.loadStatistics();
        });
        // onWillStart(async () => {
        //     const result = await this.statisticsService.loadStatistics();
        //     if (result) {
        //         this.statistics = {
        //             new_orders: result.nb_new_orders,
        //             total_sales: result.total_amount,
        //             avgerage_quantity: result.average_quantity,
        //             cancelled_orders: result.nb_cancelled_orders,
        //             avg_order_time: result.average_time,
        //             orders_by_size: result.orders_by_size
        //         };
        //     }
        // });
    }
    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
