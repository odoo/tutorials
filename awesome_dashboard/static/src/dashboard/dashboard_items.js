/* @odoo-module*/

import { NumberCard } from "./number_card/number_card"

import { PieChartCard } from "./piechart_card/piechart_card"

export const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "'Average time for an order to get from 'new' to 'sold' or 'canceled'",
            value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of canceled orders",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Number of canceled orders this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_amount",
        description: "Total number of new orders",
        Component: NumberCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Total number of new orders this month",
            value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        // size and props are optionals
        size: 1,
        props: (data) => ({
            title: "Shirt orders by size",
            data: data.orders_by_size
        }),
    },

]