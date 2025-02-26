import { NumberCard } from "../item/numbercard";
import { PieChartCard } from "../item/piechartcard";


export const items = [
    {
        id: "average_time",
        description: "Average time for an order",
        active: true,
        Component: NumberCard,
        props: (data) => ({
            size: 1,
            title: "Monthly average time for an order",
            value: data.average_time
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled orders",
        active: true,
        Component: NumberCard,
        props: (data) => ({
            size: 1,
            title: "Cancelled orders",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of tshirt",
        active: true,
        Component: NumberCard,
        props: (data) => ({
            size: 1,
            title: "Average amount of tshirt",
            value: data.average_quantity
        }),
    },
    {
        id: "nb_new_orders",
        description: "Cancelled orders",
        active: true,
        Component: NumberCard,
        props: (data) => ({
            size: 1,
            title: "Cancelled orders this month",
            value: data.nb_new_orders
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by size",
        active: true,
        Component: PieChartCard,
        props: (data) => ({
            size: 1,
            title: "Orders by size",
            data: data.orders_by_size
        }),
    }
]
