import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "New Orders",
    Component: NumberCard,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
        color: "primary",
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    props: (data) => ({
        title: "Total Amount",
        value: data.total_amount,
        color: "success",
    }),
});

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average Quantity",
    Component: NumberCard,
    props: (data) => ({
        title: "Average Quantity",
        value: data.average_quantity,
        color: "info",
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders,
        color: "danger",
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average Time",
    Component: NumberCard,
    props: (data) => ({
        title: "Avg Time (hours)",
        value: data.average_time,
        color: "warning",
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "T-Shirt Sizes",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "T-Shirt Sizes",
        data: data.orders_by_size,
    }),
});
