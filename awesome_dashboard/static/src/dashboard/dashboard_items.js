import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

export const items = [
    {
        id: "average_quantity",
        description: "Average amount",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average time",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'send' or 'canceled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "New orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Canceled orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of canceled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by size",
        Component: PieChartCard,
        size: 3,
        props: (data) => ({
            title: "Shirt orders by size",
            value: data.orders_by_size,
        }),
    },
];
