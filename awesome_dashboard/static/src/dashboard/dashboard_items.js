/** @odoo-module **/
import { NumberCard } from "./cards/number_card";
import { PieChart } from "./pieChart/pie_chart";
import { registry } from "@web/core/registry";

export const items = [
    {
        id: "average_quantity",
        description: "Average amount of T-shirt by order this month",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description:
            "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title:
                "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 1.25,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders pie chart",
        Component: PieChart,
        props: (data) => ({
            datasets: [{ data: Object.values(data.orders_by_size) }],
            labels: Object.keys(data.orders_by_size).map((label) =>
                label.toUpperCase()
            ),
        }),
    },
];

items.forEach((item) => {
    registry.category("awesome_dashboard").add(item.id, item);
});


