import { NumberCard } from "./components/numbercard/numbercard";
import { PiechartCard } from "./components/piechartcard/piechartcard";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            desc: "Number of new orders this month",
            value: data.nb_new_orders
        }),
    },
    {
        id: "total_amount_new_order",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            desc: "Total amount of new orders this month",
            value: data.total_amount
        }),
    },
    {
        id: "avg_amount_tshirt_order",
        description: "Average amount of t-shirt ordered this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            desc: "Average amount of t-shirt ordered this month",
            value: data.average_quantity
        }),
    },
    {
        id: "cancel_order",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            desc: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "avg_time_order",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            desc: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time
        }),
    },
    {
        id: "order_by_size",
        description: "Order By Size",
        Component: PiechartCard,
        props: (data) => ({
            desc: "Order By Size",
            value: data.orders_by_size
        }),
    }
]

items.forEach(item =>{
    registry.category("awesome_dashboard").add(item.id, item)
})
