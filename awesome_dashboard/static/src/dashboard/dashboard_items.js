import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const items = [
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        })
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders
        })
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        })
    },
    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time
        })
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            data: data.orders_by_size
        })
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
