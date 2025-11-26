import { registry } from "@web/core/registry";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { NumberCard } from "./number_card/number_card";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        size: 1,
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average order time",
        size: 2,
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "New orders",
        size: 2,
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Average amount of t-shirt",
        size: 1,
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total new orders",
        size: 1,
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        size: 2,
        Component: PieChartCard,
        props: (data) => ({
            title: "Shirt orders by size",
            value: data.orders_by_size,
        }),
    },
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
