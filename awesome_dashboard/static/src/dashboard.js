import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard-item/dashboard-item"
import { NumberCard } from "./number-card/number-card"
import { PieChartCard } from "./pie-chart/pie-chart-card"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));

        // Dashboard items
        this.items = [
            {
                id: "nb_new_orders",
                description: "Number of new orders this month",
                component: NumberCard,
                props: (data) => ({
                    title: "Number of new orders this month",
                    value: data.nb_new_orders,
                }),
            },
            {
                id: "total_amount",
                description: "Total amount of new orders this month",
                component: NumberCard,
                props: (data) => ({
                    title: "Total amount of new orders this month",
                    value: data.total_amount,
                }),
            },
            {
                id: "average_quantity",
                description: "Average amount of t-shirt by order this month",
                component: NumberCard,
                props: (data) => ({
                    title: "Average amount of t-shirt by order this month",
                    value: data.average_quantity,
                }),
            },
            {
                id: "nb_cancelled_orders",
                description: "Number of cancelled orders this month",
                component: NumberCard,
                props: (data) => ({
                    title: "Number of cancelled orders this month",
                    value: data.nb_cancelled_orders,
                }),
            },
            {
                id: "average_time",
                description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
                component: NumberCard,
                props: (data) => ({
                    title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
                    value: data.average_time,
                }),
            },
            {
                id: "orders_by_size",
                description: "Ordered T-shirts by size",
                component: PieChartCard,
                size: 2,
                props: (data) => ({
                    title: "Ordered T-shirts by size",
                    value: data.orders_by_size,
                }),
            },
        ];
    }

    actionCustomers() {
        this.action.doAction("base.action_partner_form", { viewType: "kanban" });
    }

    actionLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
