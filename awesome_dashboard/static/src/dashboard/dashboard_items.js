import { NumberCard } from "./NumberCard";
import { PieChartCard } from "./PieChartCard";
import { registry } from "@web/core/registry";

registry.category("awesome_dashboard").add("nb_new_orders", {
    id: "nb_new_orders",
    description: "Number of new products this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1.5,
    props: (data) => ({
        label: "Number of new products this month",
        value: data.nb_new_orders,
    }),
})
registry.category("awesome_dashboard").add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1.5,
    props: (data) => ({
        label: "Total amount of new orders this month",
        value: data.total_amount,
    }),
})
registry.category("awesome_dashboard").add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt by order this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1.5,
    props: (data) => ({
        label: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
})
registry.category("awesome_dashboard").add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Number of cancelled orders this month",
    Component: NumberCard,
    // size and props are optionals
    size: 1.5,
    props: (data) => ({
        label: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders,
    }),
})
registry.category("awesome_dashboard").add("average_time", {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    // size and props are optionals
    size: 1.5,
    props: (data) => ({
        label: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
    }),
})
registry.category("awesome_dashboard").add("orders_by_size", {
    id: "orders_by_size",
    description: "Shirt orders by size",
    Component: PieChartCard,
    // size and props are optionals
    size: 1.5,
    props: (data) => ({
        label: "Shirt orders by size",
        data: data.orders_by_size,
    }),
})