import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card.js";
import { PieChartCard } from "./pie_chart/pie_chart_card.js";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            description: "Average amount of t-shirt ordered this month",
            data: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            data: data.average_time,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            description: "Number of cancelled orders this month",
            data: data.nb_cancelled_orders,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            description: "Number of new orders this month",
            data: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            description: "Total amount of new orders this month",
            data: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Average amount of t-shirt",
        Component: PieChartCard,
        size: 1.5,
        props: (data) => ({
            description: "Shirt orders by size",
            data: data.orders_by_size,
        }),
    },
];

registry.category("awesome_dashboard").add("awesome_dashboard.items", items);
