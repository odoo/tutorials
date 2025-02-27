import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average quantity of t-shirt by order",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amout of t-shirt by order this month",
            value: data?.average_quantity ?? 0,
        }),
    },
    {
        id: "average_time",
        description: "Average time to deliver",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average time for an order to go from new to send or cancelled",
            value: data?.average_time ?? 0,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data?.nb_new_orders ?? 0,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data?.nb_cancelled_orders ?? 0,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data?.total_amount ?? 0,
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Shirt orders by size",
            values: data?.orders_by_size,
        }),
    }
]

items.forEach((item) => {
    registry.category("awesome_dashboard.dashboard_items").add(item.id, item);
});
