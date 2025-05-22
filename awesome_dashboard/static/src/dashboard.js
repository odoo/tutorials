/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "@awesome_dashboard/dashboard_item";
import { PieChart } from "@awesome_dashboard/charts/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard_statistics"));
    }

    get data() {
        return {
            average_quantity: this.stats.data.average_quantity,
            average_time: this.stats.data.average_time,
            nb_cancelled_orders: this.stats.data.nb_cancelled_orders,
            nb_new_orders: this.stats.data.nb_new_orders,
            orders_by_size: {
                data: {
                    datasets: [
                        {
                            data: [
                                this.stats.data.orders_by_size.m,
                                this.stats.data.orders_by_size.s,
                                this.stats.data.orders_by_size.xl,
                            ],
                        },
                    ],
                    labels: ["M", "S", "XL"],
                },
            },
            total_amount: this.stats.data.total_amount,
        };
    }

    onClickCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            target: "current",
            res_model: "res.partner",
            views: [[false, "kanban"]],
        });
    }

    onClickLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
