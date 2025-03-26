/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboard_item";
import { rpc } from "@web/core/network/rpc";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem};

    setup() {
        this.action = useService("action");
        // console.log("hello");
        // this.rpc = useService("rpc");

        this.state = useState({
            statistics: {
                new_orders: 0,
                total_sales: 0,
                avg_tshirts_per_order: 0,
                cancelled_orders: 0,
                avg_order_time: 0,
            }
        });

        onWillStart(async () => {
            try {
                const result = await rpc("/awesome_dashboard/statistics", {});
                if (result) {
                    this.state.statistics = {
                        new_orders: result.nb_new_orders || 0,
                        total_amount: result.total_amount  || 0,
                        avg_tshirt_per_order: result.average_quantity   || 0,
                        cancelled_orders: result.nb_cancelled_orders || 0,
                        avg_order_time: result.average_time || 0,
                    };
                }
            } catch (error) {
                console.error("Failed to fetch statistics:", error);
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
AwesomeDashboard.template = "awesome_dashboard.AwesomeDashboard";

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
