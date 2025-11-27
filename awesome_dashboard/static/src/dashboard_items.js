import { registry } from "@web/core/registry";
import { NumberCard } from "./dashboard/number_card";
import { PieChartCard } from "./dashboard/pie_chart_card";

const dashboardItemsRegistry = registry.category("awesome_dashboard.items");

dashboardItemsRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders,
    }),
});

dashboardItemsRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
    }),
});

dashboardItemsRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
});

dashboardItemsRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Number of cancelled orders this month",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders,
    }),
});

dashboardItemsRegistry.add("average_time", {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
    }),
});

dashboardItemsRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Shirt order by size",
    Component: PieChartCard,
    size: 3,
    props: (data) => ({
        title: "Shirt order by size",
        items: data.orders_by_size,
    }),
});
