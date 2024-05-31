/** @odoo-module **/

import { NumberCard } from "./dashboard_item/number_card";
import { PieChartCard } from "./dashboard_item/piechart_card";
import { registry } from "@web/core/registry";

export const useDashboardItems = () => {
    return registry.get("awesome_dashboard.dashboard_items");
}

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    }, {
        id: "average_time",
        description: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
            value: data.average_time,
        }),
    }, {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    }, {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    }, {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    }, {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            value: data.orders_by_size,
        }),
    },
];

registry.add("awesome_dashboard.dashboard_items", items);