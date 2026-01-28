import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { registry } from "@web/core/registry";

const dashboardItemsRegistry = registry.category("dashboard_items");

dashboardItemsRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    props: (stats) => ({
        title: "Average amount of t-shirts / order",
        value: stats.average_quantity,
    }),
});

dashboardItemsRegistry.add("average_time", {
    id: "average_time",
    description: "Average time for an order",
    Component: NumberCard,
    props: (stats) => ({
        title: "Average time for an order (hours)",
        value: stats.average_time,
    }),
});

dashboardItemsRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount",
    Component: NumberCard,
    props: (stats) => ({
        title: "Total amount of new orders",
        value: stats.total_amount,
    }),
});

dashboardItemsRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled orders this month",
    Component: NumberCard,
    props: (stats) => ({
        title: "Number of cancelled orders",
        value: stats.nb_cancelled_orders,
    }),
});

dashboardItemsRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "New orders",
    Component: NumberCard,
    props: (stats) => ({
        title: "Number of new orders",
        value: stats.nb_new_orders,
    }),
});

dashboardItemsRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Orders by size",
    Component: PieChartCard,
    size: 2,
    props: (stats) => ({
        title: "Shirt orders by size",
        data: stats.orders_by_size,
    }),
});
