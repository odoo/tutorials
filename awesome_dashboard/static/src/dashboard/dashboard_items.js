import { NumberCard } from "./components/numbercard/numbercard";
import { PieChartCard } from "./components/piechartcard/piechartcard";
import { registry } from "@web/core/registry";

const dashboardItems = [
    {
        id: "nb_new_orders",
        description: "new order per month",
        Component:NumberCard,
        size:2,
        props: (data) => ({
            title: "Number of new orders this month",
            number: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component:NumberCard,
        size:2,
        props: (data) => ({
            title: "Total amount of new orders this month",
            number: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt by order this month",
        Component:NumberCard,
        size:2,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            number: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component:NumberCard,
        size:2,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            number: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
        Component:NumberCard,
        size:2,
        props: (data) => ({
            title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
            number: data.average_time,
        }),
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component:PieChartCard,
        size:2,
        props: (data) => ({
            title: "Shirt orders by size",
            data: data.orders_by_size,
        }),
    },
];

dashboardItems.forEach(item =>{
    registry.category("awesome_dashboard").add(item.id, item);
});
