import { NumberCard } from "./components/number_card"
import { PieChartCard } from "./components/pie_chart_card"

export const items = [
    {
        id: "nb_new_orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({ title: "Number of new orders this month", value: data.nb_new_orders }),
    },
    {
        id: "average_time",
        Component: NumberCard,
        size: 2,
        props: (data) => ({ title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'", value: data.average_time }),
    },
    {
        id: "average_quantity",
        Component: NumberCard,
        size: 1,
        props: (data) => ({ title: "Average amount of t-shirt by order this month", value: data.average_quantity }),
    },
    {
        id: "nb_cancelled_orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({ title: "Number of cancelled orders this month", value: data.nb_cancelled_orders }),
    },
    {
        id: "total_amount",
        Component: NumberCard,
        size: 1,
        props: (data) => ({ title: "Total amount of new orders this month", value: data.total_amount }),
    },
    {
        id: "orders_by_size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({ title: "Orders by size", data: data.orders_by_size }),
    },
]
