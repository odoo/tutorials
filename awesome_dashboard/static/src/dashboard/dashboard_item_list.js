/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.4,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "total_new_orders",
        description: "Total amount of new orders",
        Component: NumberCard,
        size: 1.4,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount
        }),
        is_displayed: false,
    },
    {
        id: "cancelled_orders",
        description: "Total amount of cancelled orders",
        Component: NumberCard,
        size: 1.4,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders this month",
        Component: PieChartCard,
        size: 1.4,
        props: (data) => ({
            title: "Number of orders this month, by size",
            value: data.orders_by_size
        }),
    }
]

for (let item of items) {   
    registry.category("dashboard_items").add(item.id, item);
}
