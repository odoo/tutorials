import { registry } from "@web/core/registry";
import { NumberCard } from "./number-card/number-card";
import { PieChartCard } from "./pie-chart/pie-chart-card";

registry.category("awesome_dashboard").add("nb_new_orders", {
    id: "nb_new_orders",
    description: "Number of new orders this month",
    component: NumberCard,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders,
    }),
});

registry.category("awesome_dashboard").add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    component: NumberCard,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
    }),
});

registry.category("awesome_dashboard").add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt by order this month",
    component: NumberCard,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
});

registry.category("awesome_dashboard").add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Number of cancelled orders this month",
    component: NumberCard,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders,
    }),
});

registry.category("awesome_dashboard").add("average_time", {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    component: NumberCard,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
    }),
});

registry.category("awesome_dashboard").add("orders_by_size", {
    id: "orders_by_size",
    description: "Ordered T-shirts by size",
    component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "Ordered T-shirts by size",
        value: data.orders_by_size,
    }),
});
