import { registry } from "@web/core/registry";
import { NumberCard } from "./numbercard/number_card";
import { PieChartCard } from "./numbercard/PieChartCard";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry
    .add("average_quantity", {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    })
    .add("average_time", {
        id: "average_time",
        description: "Average order processing time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average Time for an order to go from 'new' to 'send'",
            value: data.average_time
        }),
    })
    .add("nb_new_orders", {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        }),
    })
    .add("total_amount", {
        id: "total_amount",
        description: "Total amount of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount
        }),
    })
    .add("orders_by_size", {
        id: "orders_by_size",
        description: "T-shirt size distribution",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "T-Shirt Sizes Distribution",
            data: data.orders_by_size
        }),
    });
