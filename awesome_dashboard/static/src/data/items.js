import { NumberCard } from "../cards/numbercard/numbercard";
import { PieChartCard } from "../cards/piechartcard/piechart";
import { registry } from "@web/core/registry"

const ITEMS = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt by order this month",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: 'Average amount of t-shirt by order this month',
            value: data.average_quantity,
        })
    },
    {
        id: "average_time",
        description: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled`",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: 'Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled`',
            value: data.average_time,
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: 'Number of cancelled orders this month',
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: 'Number of new orders this month',
            value: data.nb_new_orders,
        })
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: 'Total amount of new orders this month',
            value: data.total_amount,
        })
    },
    {
        id: "orders_by_size",
        description: "Graph Representation",
        Component: PieChartCard,
        props: (data) => ({
            title: 'Graph Representation',
            value: data.orders_by_size,
        })
    }
]

registry.category("awesome_dashboard.dashboard").add("awesome_dashboard.items", ITEMS);
