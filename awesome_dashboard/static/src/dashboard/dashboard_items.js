/** @odoo-module */

import { PieChartCard } from "./pie_chart_card/pie_char_card";
import { NumberCard } from "./number_card/number_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "orders_by_size",
        description: "T-Shirt Oders By Size",
        Component: PieChartCard,
        props: (data) => ({
            title: "Shirt orders by size",
            data: data.orders_by_size,
        }),
    },
    {
        id: "average_time",
        description: "Average Time of T-Shirt Orders",
        Component: NumberCard,
        props: (data) => ({
            title:
                "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
            value: data.average_time,
        }),
    },
    {
        id: "new_orders",
        description: "New T-Shirt Orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "average_quantity",
        description: "Average Amount of T-Shirt Orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "cancelled_orders",
        description: "Cancelled T-Shirt Orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total T-Shirt Orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
];

registry.category("awesome_dashboard").add("dashboard_items", items);
