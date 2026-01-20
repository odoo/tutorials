import { Piechart } from "./components/piechart/piechart";
import { NumberCard } from "./components/number_card/number_card";
import { registry } from "@web/core/registry";

const item1 = {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,

    size: 1,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity
    }),
};
const item2 = {
    id: "average_time",
    description: 'AVG time for an order to go from "new" to "sent" or "cancelled"',
    Component: NumberCard,

    size: 1,
    props: (data) => ({
        title: 'AVG time for an order to go from "new" to "sent" or "cancelled"',
        value: data.average_time
    }),
};
const item3 = {
    id: "nb_new_orders",
    description: "New orders",
    Component: NumberCard,

    size: 1,
    props: (data) => ({
        title: "New orders this month",
        value: data.nb_new_orders
    }),
};
const item4 = {
    id: "nb_cancelled_orders",
    description: "Cancelled orders",
    Component: NumberCard,

    size: 1,
    props: (data) => ({
        title: "Cancelled orders this month",
        value: data.nb_cancelled_orders
    }),
};
const item5 = {
    id: "total_amount",
    description: "Total orders",
    Component: NumberCard,

    size: 1,
    props: (data) => ({
        title: "Total orders",
        value: data.total_amount
    }),
};

const item6 = {
    id: "orders_per_size",
    description: "Shirt Orders per size",
    Component: Piechart,

    size: 1,
    props: (data) => ({
        labels: Object.keys(data.orders_by_size),
        data: Object.values(data.orders_by_size)
    }),
}

registry.category("awesome_dashboard").add("dashboard_items", [item1, item2, item3, item4, item5, item6]);
