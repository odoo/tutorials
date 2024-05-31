/** @odoo-module */

import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { NumberCard } from "./number_card/number_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Average time",
            value: data.average_time
        }),
    },
    {
        id: "new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "New orders",
            value: data.nb_new_orders
        }),
    },
    {
        id: "number_cancelled",
        description: "Number of Cancelled orders",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "number cancelled orders",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_orders",
        description: "total orders",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "total orders",
            value: data.total_amount
        }),
    },
    {
        id: "chart_sizes",
        description: "chart by size",
        Component: PieChartCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "shirt orders by size",
            value: data.orders_by_size
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});