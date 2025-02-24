/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = this.env.services.action;
        this.rpc = rpc;

        this.statistics = useState({
            averageQuantity: 0,
            averageTime: 0,
            nbCancelledOrders: 0,
            nbNewOrders: 0,
            totalAmount: 0,
            ordersBySize: { m: 0, s: 0, xl: 0 },
        });

        this.display = {
            controlPanel: {},
        };

        onWillStart(async () => {
            try {
                const result = await this.rpc("/awesome_dashboard/statistics", {});
                this.statistics.averageQuantity = result.average_quantity;
                this.statistics.averageTime = result.average_time;
                this.statistics.nbCancelledOrders = result.nb_cancelled_orders;
                this.statistics.nbNewOrders = result.nb_new_orders;
                this.statistics.totalAmount = result.total_amount;
                this.statistics.ordersBySize = result.orders_by_size;
            } catch (error) {
                console.error("Failed to load dashboard statistics:", error);
            }
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
