/** @odoo-module */

import { registry } from "@web/core/registry";
import { NumberCard } from "./numbercard/number_card";
import { PieChartCard } from "./piechartcard/piechart_card";

const dashboardRegistry = registry.category("awesome_dashboard");

const dashboardItems = [
    {
        id: "number_new_orders",
        description: "New order this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },

    {
        id: "average_new_sent_cancelled",
        description: "Average time for an order",
        Component: NumberCard,
        props: (data) => ( {
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
    },

    {
        id: "total_amount_new_orders",
        description: "Amount orders this month",
        Component: NumberCard,
        props: (data) => ( {
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },

    {
        id: "average_orders",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ( {
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },

    {
        id: "number_cancelled_order",
        description: "Cancelled orders this month",
        Component: NumberCard,
        props: (data) => ( {
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },

    {
        id: "stats_size_sold",
        description: "Shirt orders by size",
        Component: PieChartCard,
        props: (data) => ( {
            title: "Stats",
            chartData: data.orders_by_size,
        }),
    },

];

dashboardItems.forEach(item => {
    dashboardRegistry.add(item.id, item);
})
