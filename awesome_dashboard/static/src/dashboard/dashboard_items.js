/** @odoo-module */
import {NumberCard} from "./number_card/number_card";
import {PieChartCard} from "./pie_chart_card/pie_chart_card";

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
        description: "Total amount of orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders",
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average time to change state",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
            value: data.average_time,
        }),
    },
    {
        id: "pie_chart",
        description: "Pie chart of orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Orders by size",
            values: data.orders_by_size,
        })
    }
]


