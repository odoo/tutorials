import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieCard } from "./pie_card";

const item_list = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average process time",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time (in hours) processing elapsed",
            value: data.average_time
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders, this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders",
            value: data.nb_new_orders
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders",
            value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: "Number of orders by size",
        Component: PieCard,
        size: 2,
        props: (data) => ({
            title: "Number of orders by size",
            value: data.orders_by_size
        }),
    }
]

item_list.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
})
