import { registry } from "@web/core/registry";

import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average time between order creation and shipment",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average time between order creation and shipment",
            value: data.average_time,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Average time between order creation and shipment",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average time between order creation and shipment",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "orders_by_size",
        description: "Graph of t-shirt sizes ordered",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Graph of t-shirt sizes ordered",
            value: data.orders_by_size,
        }),
    },
];

items.forEach((item) => registry.category("awesome_dashboard").add(item.id, item));
