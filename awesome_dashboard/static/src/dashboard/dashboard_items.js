import { PieChartCard } from "./components/piechartcard/piechartcard";
import { NumberCard } from "./components/numbercard/numbercard";
import { registry } from "@web/core/registry"

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
           desc: "Average amount of t-shirt by order this month",
           value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
           desc: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
           value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
           desc: "Number of new orders this month",
           value: data.nb_new_orders
        }),
     },
     {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
           desc: "Number of cancelled orders this month",
           value: data.nb_cancelled_orders
        }),
     },
     {
        id: "total_amount",
        description: "Total amount of new orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
           desc: "Total amount of new orders this month",
           value: data.total_amount
        }),
     },
     {
        id: "orders_by_size",
        description: "Order by size",
        Component: PieChartCard,
        size: 1.8,
        props: (data) => ({
           desc: "Order by size",
           data: data.orders_by_size
        }),
     }
]

items.forEach(item =>{
   registry.category("awesome_dashboard").add(item.id,item)
})
