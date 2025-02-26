/** @odoo-module **/

import { PieChartCard } from "../cards/pie_chart_card";
import { NumberCard } from "../cards/number_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirts per order this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average amount of t-shirts per order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Avg. time from 'new' to 'sent/cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "New orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total amount of new orders",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            data: data.orders_by_size,
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});