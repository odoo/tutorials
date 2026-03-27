/** @odoo-module **/

import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";


const items = [
    {
        id: "number_new_orders",
        description: "new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "new orders",
            value: data.nb_new_orders,
        })
    },
    {
        id: "average_quantity",
        description: "average quantity",
        Component: NumberCard,
        props: (data) => ({
            title: "average quantity",
            value: data.average_quantity,
        })
    },
    {
        id: "average_time",
        description: "average time",
        Component: NumberCard,
        props: (data) => ({
            title: "average time between new and sent",
            value: data.average_time,
        })
    },
    {
        id: "amount_new_orders",
        description: "new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "new orders this month",
            value: data.total_amount,
        })
    },
    {
        id: "pie_chart",
        description: "orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "orders by size",
            values: data.orders_by_size,
        })
    }
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
