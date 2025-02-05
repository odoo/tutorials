/** @odoo-module **/
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { registry } from "@web/core/registry";

export const dashboardRegistry = registry.category("awesome_dashboard.items");

dashboardRegistry.add(
    "average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt by order",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "T-shirt Ordered",
        value: data,
    }),
})

dashboardRegistry.add(
    "average_time", {
    id: "average_time",
    description: "Average Time",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data,
    }),
})

dashboardRegistry.add(
    "nb_new_orders", {
    id: "nb_new_orders",
    description: "New orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Numbers of new orders this month",
        value: data,
    }),
})

dashboardRegistry.add(
    "nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Numbers of cancelled orders this month",
        value: data,
    })
})

dashboardRegistry.add(
    "total_amount", {
    id: "total_amount",
    description: "Total Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Numbers of new orders this month",
        value: data,
    }),
})

dashboardRegistry.add(
    "orders_by_size", {
    id: "orders_by_size",
    description: "Orders by size",
    Component: PieChartCard,
    size: 1.5,
    props: (data) => ({
        label: "Orders by size",
        data: data,
    }),
})