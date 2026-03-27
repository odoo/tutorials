import { NumberCard } from "./number_card/number_card"
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const dashboardItemsRegistry = registry.category("awesome_dashboard.items");

dashboardItemsRegistry.add("avg_quantity", {
    id: "avg_quantity",
    description: "Average quantity",
    Component: NumberCard,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
});

dashboardItemsRegistry.add("avg_time", {
    id: "avg_time",
    description: "Average time",
    size: 2,
    Component: NumberCard,
    props: (data) => ({
        title: "Average time for order",
        value: data.average_time,
    }),
});

dashboardItemsRegistry.add("new_orders", {
    id: "new_orders",
    description: "New orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Number of new orders",
        value: data.nb_new_orders,
    }),
});
dashboardItemsRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Cancelled orders",
        value: data.nb_cancelled_orders,
    }),
});
dashboardItemsRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount",
    Component: NumberCard,
    props: (data) => ({
        title: "Total amount",
        value: data.total_amount,
    }),
});

dashboardItemsRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Orders by size",
    size: 2,
    Component: PieChartCard,
    props: (data) => ({
        title: "Shirt orders by size",
        data: data.orders_by_size,
    }),
});
