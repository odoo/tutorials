/** @odoo-module **/

import { registry } from "@web/core/registry";
import { AwesomeDashboardNumberCard } from "./dashboard_number_card"
import { AwesomeDashboardPieChart } from "./dashboard_pie_chart"

const dashboardItems = [
    {
        id: "average_quantity",
        description: "Average quantity of t-shirts",
        Component: AwesomeDashboardNumberCard,
        props: (data) => ({
            title: "Average quantity of t-shirts by order this month",
            value: data.average_quantity,
        })
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: AwesomeDashboardNumberCard,
        props: (data) => ({
            title: "Average time for an order to be processed",
            value: data.average_time,
        })
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: AwesomeDashboardNumberCard,
        props: (data) => ({
            title: "Number of new orders, this month",
            value: data.nb_new_orders,
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: AwesomeDashboardNumberCard,
        props: (data) => ({
            title: "Number of cancelled orders, this month",
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "total_amount",
        description: "Total amount of orders",
        Component: AwesomeDashboardNumberCard,
        props: (data) => ({
            title: "Total amount of orders, this month",
            value: data.total_amount,
        })
    },
    {
        id: "orders_by_size",
        description: "Shirt orders",
        Component: AwesomeDashboardPieChart,
        props: (data) => ({
            title: "Shirt orders, by size",
            data: data.orders_by_size,
        })
    }
]

dashboardItems.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
