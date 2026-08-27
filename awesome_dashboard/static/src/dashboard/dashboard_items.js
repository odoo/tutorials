import { NumberCard } from "./numberCard/number_card";
import { PieChartCard } from "./pieChartCard/piechart_card";
import { registry } from "@web/core/registry";


const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        })
    },
    {
        id: "average_time",
        description: "Average delivery time",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average time it takes to deliver a t-shirt",
            value: data.average_time
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of orders that were cancelled.",
            value: data.nb_cancelled_orders
        })
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of orders that were new.",
            value: data.nb_new_orders
        })
    },
    {
        id: "total_amount",
        description: "Total amount of orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total number of orders",
            value: data.total_amount
        })
    },
    {
        id: "pie_chart",
        description: "Orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Display the orders in a pie chart by size",
            value: data.orders_by_size
        })
    },
]

registry.category("awesome_dashboard").add("items", items);
