/** @odoo-module **/
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

export const items = [
    {
        id: "new_orders",
        description: "New orders this month",
        Component: NumberCard,
        props: (stats) => ({
            title: "New Orders",
            value: stats.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount this month",
        Component: NumberCard,
        props: (stats) => ({
            title: "Total Amount",
            value: stats.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average T-Shirts per order",
        Component: NumberCard,
        props: (stats) => ({
            title: "Avg T-Shirts / Order",
            value: stats.average_quantity,
        }),
    },
    {
        id: "cancelled_orders",
        description: "Cancelled orders this month",
        Component: NumberCard,
        props: (stats) => ({
            title: "Cancelled Orders",
            value: stats.nb_cancelled_orders,
        }),
    },
    {
        id: "avg_time",
        description: "Average processing time",
        Component: NumberCard,
        props: (stats) => ({
            title: "Avg Processing Time (hours)",
            value: stats.average_time,
        }),
        size: 2,
    },
    {
        id: "tshirt_sizes",
        description: "T-Shirt sizes sold",
        Component: PieChartCard,
        props: (stats) => ({
            title: "T-Shirt Sizes Sold",
            data: stats.orders_by_size,
        }),
        size: 2,
    },
];