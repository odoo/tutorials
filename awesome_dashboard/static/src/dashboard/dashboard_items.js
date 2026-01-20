import { registry } from "@web/core/registry";
import { NumberCard } from "./card/number_card";
import { PieChartCard } from "./card/pie_chart_card";

const items = [
    {
        id: "avg_amount",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            data: data.average_quantity,
        }),
    },
    {
        id: "avg_time",
        description: "Average time for an order to go",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            data: data.average_time,
        }),
    },
    {
        id: "new_order",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            data: data.nb_new_orders,
        }),
    },
    {
        id: "cancelled_order",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            data: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_order",
        description: "Total amount of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            data: data.total_amount,
        }),
    },
    {
        id: "order_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            data: data.orders_by_size,
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});