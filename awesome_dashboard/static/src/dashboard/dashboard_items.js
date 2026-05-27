import { registry } from "@web/core/registry";
import { NumberCard } from "../number_card/number_card";
import { PiechartCard } from "../piechart_card/piechart_card";

export const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirts",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average order time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to reach a final state.",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "New orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PiechartCard,
        props: (data) => ({
            title: "Shirt orders by size",
            values: data.orders_by_size,
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
