import { PieChartCard } from "./piechartcard";
import { NumberCard } from "./numbercard";
import { registry } from "@web/core/registry"

export const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt by order this month",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        size: 2.2,
        props: (data) => ({
            title: "Avg. time: 'new' ➔ 'sent'/'cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 1.4,
        props: (data) => ({
            title: "New Orders This Month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Cancelled Orders This Month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "sales_distribution",
        description: "Sales Distribution by T-Shirt Size",
        Component: PieChartCard,
        size: 1.6,
        props: (data) => ({
            title: "Sales Distribution by Size",
            value: data,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 1.6,
        props: (data) => ({
            title: "Total New Order Amount (₹)",
            value: data.total_amount,
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});