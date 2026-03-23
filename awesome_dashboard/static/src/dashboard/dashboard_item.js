/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./piechart_card/piechart_card";

const dashboardItems = [
    {
        id: "average_quantity",
        description: "Average T-Shirts",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average t-shirt per order",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average processing time",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average processing time",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "New Orders",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "New Orders",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled Orders",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Cancelled Orders",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total Amount",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Total Amount",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by Size",
        Component: PieChartCard,
        size: 3,
        props: (data) => ({
            title: "Orders by Size",
            data: data.orders_by_size || {},
        }),
    },
];


const dashboardItemRegistry = registry.category("awesome_dashboard");

for (const item of dashboardItems) {
    dashboardItemRegistry.add(item.id, item);
}
