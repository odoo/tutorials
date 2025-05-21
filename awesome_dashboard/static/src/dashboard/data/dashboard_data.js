/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PieChartCard } from "@awesome_dashboard/dashboard/cards/pie_chart_card";
import { NumberCard } from "@awesome_dashboard/dashboard/cards/number_card";

registry.category("awesome_dashboard").add("data", {
    average_quantity: {
        Component: NumberCard,
        props: (stats) => ({
            title: "Average amount of t-shirt by order this month",
            value: stats.data.average_quantity,
        }),
        active: true,
    },
    average_time: {
        Component: NumberCard,
        props: (stats) => ({
            title: "Average time to deliver an order this month",
            value: stats.data.average_time,
        }),
        active: true,
    },
    nb_cancelled_orders: {
        Component: NumberCard,
        size: 2.5,
        props: (stats) => ({
            title: "Number of cancelled orders this month",
            value: stats.data.nb_cancelled_orders,
        }),
        active: true,
    },
    nb_new_orders: {
        Component: NumberCard,
        size: 2.5,
        props: (stats) => ({
            title: "Number of new orders this month",
            value: stats.data.nb_new_orders,
        }),
        active: true,
    },
    total_amount: {
        Component: NumberCard,
        size: 2.5,
        props: (stats) => ({
            title: "Total amount of orders this month",
            value: stats.data.total_amount,
        }),
        active: true,
    },
    orders_by_size: {
        Component: PieChartCard,
        props: (stats) => ({
            title: "Orders by size",
            chart: {
                data: {
                    datasets: [
                        {
                            data: [
                                stats.data.orders_by_size.m,
                                stats.data.orders_by_size.s,
                                stats.data.orders_by_size.xl,
                            ],
                        },
                    ],
                    labels: ["M", "S", "XL"],
                },
            },
        }),
        active: true,
    },
});
