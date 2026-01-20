import { NumberCard } from "./dashboard/numbercard";
import { PieChartCard } from "./dashboard/piechart_card";
import { registry } from "@web/core/registry";

const awesomeDashboardRegistry = registry.category("awesome_dashboard");

const items = [
    {
        id: "average_quantity",
        description: "Average amount of T-shirts per order",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "processing_time",
        description: "Average Processing Time",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled",
            value: data.average_time,
        }),
    },
    {
        id: "new_orders",
        description: "New Orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "cancelled_orders",
        description: "Cancelled Orders",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount", 
        description: "Total Amount",
        Component: NumberCard,
        size: 1.5,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "size_distribution",
        description: "Size Distribution",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Size Distribution",
            sizes: Object.keys(data.orders_by_size), 
            quantities: Object.values(data.orders_by_size),
        }),
    },
];

items.forEach((item) => {
    awesomeDashboardRegistry.add(item.id, item);
});
