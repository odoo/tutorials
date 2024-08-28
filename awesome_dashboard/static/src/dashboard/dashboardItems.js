/** @odoo-module **/

import {NumberCard} from "./cards/numberCard"
import {PieChartCard} from "./cards/pieChartCard";
import {registry} from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average quantity",
        Component: NumberCard,
        props: (data) => ({
            title: "Average quantity",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time",
            value: data.average_time
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders",
            value: data.nb_new_orders
        }),
    },
    {
        id: "total_amount",
        description: "Total amount",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount",
            value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by size",
        Component: PieChartCard,
        props: (data) => ({
            title: "Orders by size",
            values: data.orders_by_size
        }),
    },

]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
})
