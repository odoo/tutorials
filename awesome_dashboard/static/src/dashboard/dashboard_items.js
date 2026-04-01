import { registry } from "@web/core/registry";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    title: "Average Quantity",
    props: (data) => data.average_quantity,
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    title: "Average Time",
    props: (data) => data.average_time,
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    title: "Cancelled Orders",
    props: (data) => data.nb_cancelled_orders,
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    title: "New Orders",
    props: (data) => data.nb_new_orders,
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    title: "Total Amount",
    props: (data) => data.total_amount,
});

dashboardRegistry.add("pie_chart", {
    id: "pie_chart",
    title: "Orders by Size",
    type: "chart",
    props: (data) => data.orders_by_size,
});