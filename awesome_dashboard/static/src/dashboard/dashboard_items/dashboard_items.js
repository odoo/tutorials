/** @odoo-module **/

import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { registry } from "@web/core/registry";

export const dashboardRegistry = registry.category("awesome_dashboard.items");

dashboardRegistry.add(
    "nb_new_orders", {
    id: "nb_new_orders",
    description: "Numbers of new orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Numbers of new orders this month",
        value: data.nb_new_orders,
    }),
})

dashboardRegistry.add(
    "total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
    }),
})

dashboardRegistry.add(
    "average_state_change_time", {
    id: "average_state_change_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
    }),
})

dashboardRegistry.add(
    "average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt by order this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
})

dashboardRegistry.add(
    "nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Numbers of cancelled orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Numbers of cancelled orders this month",
        value: data.nb_cancelled_orders,
    })
})

dashboardRegistry.add(
    "orders_by_size", {
    id: "orders_by_size",
    description: "Orders by size",
    Component: PieChartCard,
    size: 6,
    props: (data) => ({
        label: "Orders by size",
        data: data.orders_by_size,
    }),
})

