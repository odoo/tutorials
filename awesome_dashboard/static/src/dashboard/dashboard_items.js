import { NumberCard } from "./numbercard/number_card";
import { PieChartCard } from "./piechartcard/pirchart_card";

export const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of tees ordered this month",
            value: data.average_quantity,
        })
    },

    {
        id: "average_time",
        description: "Average time of an order",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        })
    },

    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        })
    },

    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        })
    },

    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        })
    },

    {
        id: "orders_pir_chart",
        description: "Shirt order by size",
        Component: PieChartCard,
        props: (data) => ({
            title: "Shirt order by size",
            data: data.orders_by_size,
        })
    },

]