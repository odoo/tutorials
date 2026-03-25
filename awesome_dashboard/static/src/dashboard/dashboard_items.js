import { DashboardCard } from "./dashboard_card";
import { PieChart } from "./pie_chart";
import { registry } from "@web/core/registry";

const dashboardItemRegistry = registry.category("awesome_dashboard");

dashboardItemRegistry.add("orders", {
    id: "orders",
    description: "Number of new order",
    Component: DashboardCard,
    size: 1,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
    }),
});

dashboardItemRegistry.add("total", {
    id: "total",
    description: "Total amount",
    Component: DashboardCard,
    size: 1,
    props: (data) => ({
        title: "Total Amount",
        value: data.total_amount,
    }),
});

dashboardItemRegistry.add("sizes", {
    id: "sizes",
    description: "Orders by size",
    Component: PieChart,
    size: 2,
    props: (data) => ({
        data: data.orders_by_size,
    }),
});
