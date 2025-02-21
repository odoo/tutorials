import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export const DASHBOARD_ITEMS = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt by order this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        })
    },
    {
        id: "average_time",
        description: "Average time for an order to be done",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        })
    },
    {
        id: "cancelled_orders",
        description: "Cancelled orders this month this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "number_new_orders",
        description: "New orders this month this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        })
    },
    {
        id: "amount_new_orders",
        description: "amount orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        })
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            value: data.orders_by_size,
        })
    }
]
