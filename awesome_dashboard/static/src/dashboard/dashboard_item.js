import { registry } from "@web/core/registry";
import { NumberCard } from "./NumberCard/number_card";
import { PieChartCard } from "./PieChartCard/pie_chart_card";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    size: 1.3,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Shirt Orders by Size",
    Component: PieChartCard,
    size: 4,
    props: (data) => ({
        title: "Shirt Orders by Size",
        data: data.orders_by_size,
    }),
});
