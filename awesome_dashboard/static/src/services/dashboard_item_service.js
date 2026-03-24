import { NumberCard } from "../dashboard/number_card/number_card";
import { PieChart } from "../dashboard/charts/pie_chart.js";
import { registry } from '@web/core/registry';

const dashboartItemKey = [
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
        id: "orders_by_size",
        description: "Shirt Orders by Size",
        Component: PieChart,
        size: 1,
        props: (data) => ({
            title: "Shirt Orders by Size",
            value: data.orders_by_size,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
            value: data.average_time,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
];

for (let i = 0; i < dashboartItemKey.length; i++) {
    const element = dashboartItemKey[i];
    registry.category("awesome_dashboard").add(`item${i + 1}`, element);
}
