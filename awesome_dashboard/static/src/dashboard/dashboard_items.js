import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export const items = [
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of T-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of T-shirt per order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of canceled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of canceled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average order time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'canceled'",
            value: data.average_time,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "T-shirt orders by size",
            stats: data.orders_by_size,
        }),
    },
];
