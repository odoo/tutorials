import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card"
import { PieChartCard } from "./pie_chart/pie_chart_card"

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        description: "Average amount of t-shirt by order this month",
        data: data.average_quantity,
    }),
});
dashboardRegistry.add("new_orders", {
    id: "new_orders",
    description: "New orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        description: "Number of new orders this month",
        data: data.nb_new_orders,
    }),
});
dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        description: "Number of cancelled orders this month",
        data: data.nb_cancelled_orders,
    }),
});
dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total order amount",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        description: "Total amount of new orders this month",
        data: data.total_amount,
    }),
});
dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        data: data.average_time,
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        description: "Shirt orders by size",
        data: data.orders_by_size,
    }),
});
