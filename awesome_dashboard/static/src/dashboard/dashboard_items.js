
import { NumberCard } from "./NumberCard/number_card";
import { PieChart } from "./PieChartCard/pie_chart";

export const dashboardCards = [
    {
        id: "nb_new_orders",
        description: "New t-shirt orders this month.",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "New orders this month.",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Total amount of new order this month",
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt.",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled orders this month.",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to reach conclusion (sent or cancelled).",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "orders_by_size",
        description: "T-shirt orders grouped by their size.",
        Component: PieChart,
        size: 2,
        props: (data) => ({
            title: "T-shirt order by size",
            value: data.orders_by_size,
        }),
    }
]
