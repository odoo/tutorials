import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./piechart_card/piechart_card";

export const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order",
            value: data.average_quantity,
        })
    },
    {
        id: "number_new_orders",
        description: "New orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders",
            value: data.nb_new_orders,
        })
    },
    {
        id: "amount_new_orders",
        description: "amount orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders",
            value: data.total_amount,
        })
    },
    {
        id: "cancelled_orders",
        description: "Cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders",
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        })
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            values: data.orders_by_size,
        })
    }
]
