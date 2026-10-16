import { registry } from "@web/core/registry";
import { NumberCard } from "./components/number_card";
import { PieChartCard } from "./components/pie_chart_card";

const dashboardItemRegistry = registry.category("awesome_dashboard.items");

dashboardItemRegistry.add("orders_count", {
    id: "orders_count",
    description: "Orders count",
    Component: NumberCard,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
    }),
});

dashboardItemRegistry.add("orders_amount", {
    id: "orders_amount",
    description: "Orders amount",
    Component: NumberCard,
    props: (data) => ({
        title: "Total Amount",
        value: data.total_amount,
    }),
});

dashboardItemRegistry.add("avg_quantity", {
    id: "avg_quantity",
    description: "Average quantity",
    Component: NumberCard,
    props: (data) => ({
        title: "Avg T-Shirts",
        value: data.average_quantity,
    }),
});

dashboardItemRegistry.add("average_time", {
    id: "average_time",
    description: "average time",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "average time",
        value: data.average_time,
    }),
});

dashboardItemRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders,
    }),
});

dashboardItemRegistry.add("pie_chart", {
    id: "pie_chart",
    description: "T-shirt sizes",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "Ordered by Size",
        data: data.orders_by_size,
    }),
});
