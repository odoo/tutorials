import { NumberCard } from "../number_card/number_card";
import { PieChartCard } from "../pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";


const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
           title: "Average amount of t-shirt by order this month",
           value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'send' or 'cancelled'",
        Component: NumberCard,
        // size and props are optionals
        size: 2,
        props: (data) => ({
           title: "Average time for an order to go from 'new' to 'send' or 'cancelled'",
           value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
           title: "Number of new orders this month",
           value: data.nb_new_orders
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
           title: "Number of cancelled orders this month",
           value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
           title: "Total amount of new orders this month",
           value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        // size and props are optionals
        size: 2,
        props: (data) => ({
           title: "Shirt orders by size",
           data: data.orders_by_size
        }),
    },
];

for (let item of items) {
    registry.category("awesome_dashboard").add(item.id, item);
}
