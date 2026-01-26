import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChart } from "./pie_chart/pie_chart";

export const items = [
    {
        id: "new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "New Orders",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total Amount",
            value: `${data.total_amount} €`,
        }),
    },
    {
        id: "avg_tshirt",
        description: "Average number of t-shirts per order",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Avg T-Shirts/Order",
            value: data.average_quantity,
        }),
    },
    {
        id: "cancelled",
        description: "Number of cancelled orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Cancelled Orders",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "avg_time",
        description: "Average time from new to sent",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Avg Time (New to Sent)",
            value: `${data.average_time} Days`,
        }),
    },
    {
        id: "pie_chart",
        description: "Pie chart of shirts orders by size",
        Component: PieChart,
        size: 2,
        props: (data) => ({
            title: "Pie Chart of shirts orders by size",
            data: data.orders_by_size,
        }),
    },
];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
