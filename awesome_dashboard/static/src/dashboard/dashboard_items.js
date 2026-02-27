import { dashboardItemRegistry } from "./dashboard_registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

dashboardItemRegistry.add("new_orders", {
    id: "new_orders",
    description: "New orders this month",
    Component: NumberCard,
    props: (stats) => ({
        title: "New Orders",
        value: stats.nb_new_orders,
    }),
});

dashboardItemRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount this month",
    Component: NumberCard,
    props: (stats) => ({
        title: "Total Amount",
        value: stats.total_amount,
    }),
});

dashboardItemRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average T-Shirts per order",
    Component: NumberCard,
    props: (stats) => ({
        title: "Avg T-Shirts / Order",
        value: stats.average_quantity,
    }),
});

dashboardItemRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled orders this month",
    Component: NumberCard,
    props: (stats) => ({
        title: "Cancelled Orders",
        value: stats.nb_cancelled_orders,
    }),
});

dashboardItemRegistry.add("avg_time", {
    id: "avg_time",
    description: "Average processing time",
    Component: NumberCard,
    size: 2,
    props: (stats) => ({
        title: "Avg Processing Time (hours)",
        value: stats.average_time,
    }),
});

dashboardItemRegistry.add("tshirt_sizes", {
    id: "tshirt_sizes",
    description: "T-Shirt sizes sold",
    Component: PieChartCard,
    size: 2,
    props: (stats) => ({
        title: "T-Shirt Sizes Sold",
        data: stats.orders_by_size,
    }),
});