/** @odoo-module **/

import { NumberCard } from "../cards/number_card"
import { PieChartCard } from "../cards/pie_chart_card"

export const items = [
    {
        id: "average_amount_t_shirt",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "average_amount_time_order",
        description: "Average time for an order",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time
        }),
    },
    {
        id: "new_order",
        description: "Number of new order",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.average_time
        }),
    },
    {
        id: "cancelled_order",
        description: "Number of cancelled orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_orders",
        description: "Number of total orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount
        }),
    },
    {
        id: "pie_chart",
        description: "Shirt order by size",
        Component: PieChartCard,
        props: (data) => ({
            title: "Shirt order by size",
            value: data.orders_by_size
        }),
    },
]
