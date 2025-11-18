import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChart } from "./pie_chart/pie_chart";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average to time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "New orders this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled orders this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Amount orders this month",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChart,
        props: (data) => ({
            label: "Total amount of new orders this month",
            data: data.orders_by_size,
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard_items").add(item.id, item);
});
