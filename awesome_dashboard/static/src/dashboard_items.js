import {NumberCard} from "./NumberCard";
import {PieChartCard} from "./PieChartCard";
import {registry} from "@web/core/registry";

export const items = [{
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    // size and props are optionals
    size: 3,
    props: (data) =>
        ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
}, {
    id: "average_time",
    description: "Average time",
    Component: NumberCard,
    // size and props are optionals
    size: 1,
    props: (data) =>
        ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
}, {
    id: "nb_new_orders",
    description: "New order this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1,
    props: (data) =>
        ({
            title: "Number of new order this month",
            value: data.nb_new_orders
            ,
        }),
}, {
    id: "nb_cancelled_orders",
    description: "Number of canceled order this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1,
    props: (data) =>
        ({
            title: "Number of canceled order this month",
            value: data.nb_cancelled_orders,
        }),
}, {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1,
    props: (data) =>
        ({
            title: "Total amount of new orders this month",
            value: data.total_amount
            ,
        }),
}, {
    id: "orders_by_size",
    description: "Order by sie",
    Component: PieChartCard,
    // size and props are optionals
    size: 2,
    props: (data) =>
        ({
            title: "Shirts orders by size",
            data: data.orders_by_size,
        }),
}];


for (const item of items) {
    registry.category("awesome_dashboard.items").add(item.id, item)
}
