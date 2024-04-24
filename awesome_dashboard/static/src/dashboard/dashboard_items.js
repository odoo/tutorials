/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.2,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time for order",
        Component: NumberCard,
        size: 1.7,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'canceled",
            value: data.average_time
        }),
    },
    {
        id: "number_new_orders",
        description: "Number new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        }),
    },
    {
        id: "number_cancelled",
        description: "Number cancelled orders this month",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_orders",
        description: "Total new orders this month",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount
        }),
    },
    {
        id: "pie_chart_sizes",
        description: "Shirt orders by size",
        Component: PieChartCard,
        // size and props are optionals
        size: 1.5,
        props: (data) => ({
            title: "Shirt orders by size",
            value: data.orders_by_size
        }),
    },
];

for (const item of items) {
    registry.category("awesome_dashboard").add(item.id, item);
}
