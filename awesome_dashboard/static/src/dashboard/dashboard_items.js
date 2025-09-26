import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export const items = [
    {
        id: "average_quantity",
        description: "Average amount",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average Time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average Time",
            value: data.average_time
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
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "ANumber of cancelled orders",
            value: data.nb_cancelled_orders
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
        id: "pie_chart",
        description: "Shirts orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirts orders by size",
            value: data.orders_by_size
        }),
    },
];