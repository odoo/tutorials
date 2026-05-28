import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const dashRegistry = registry.category("awesome_dashboard");

dashRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders,
    }),
});

dashRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: `Rs.${data.total_amount}`,
    }),
});

dashRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirts by order",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
});

dashRegistry.add("average_time", {
    id: "average_time",
    description: "Average time from 'new' to closed",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to closed",
        value: data.average_time,
    }),
});

dashRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Number of cancelled orders this month",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders,
    }),
});

dashRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Orders by Size Distribution",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "Orders by Size",
        chart_data: data.orders_by_size,
    }),
});
