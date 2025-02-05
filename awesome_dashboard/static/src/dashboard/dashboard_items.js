import { registry } from "@web/core/registry";
import {NumberCard} from './NumberCard/NumberCard'
import {PieChartCard} from './PieChartCard/PieChartCard'

const items = [
    {
        id: "1",
        description: "Average amount of t-shirt by ordet this month",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Average amount of t-shirt by ordet this month",
            value: data.average_quantity
        }),
    },
    {
        id: "2",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time
        }),
    },
    {
        id: "3",
        description: "Number of new order this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of new order this month",
            value: data.nb_new_orders
        }),
    },
    {
        id: "4",
        description: "Number of Cancelled order this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of Cancelled order this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "5",
        description: "Total amount of new order this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total amount of new order this month",
            value: data.total_amount
        }),
    },
    {
        id: "6",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 1.3,
        props: (data) => ({
            title: "Shirt orders by size",
            labels: Object.keys(data?.orders_by_size),
            data: Object.values(data?.orders_by_size)
        }),
    },
]

registry.category('awesome_dashboard').add('items', items)
