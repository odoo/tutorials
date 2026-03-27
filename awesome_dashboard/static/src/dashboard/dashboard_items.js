import { _t } from "@web/core/l10n/translation";
import { NumberCard } from "./numberCard/numberCard";
import { PieChartCard } from "./pieChartCard/pieChartCard";
import { registry } from "@web/core/registry";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average amount of t-shirts"),
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: _t("Average Quantity"),
        value: data.average_quantity
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average time for an order"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average Time"),
        value: data.average_time
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Number of cancelled orders"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Cancelled Orders"),
        value: data.nb_cancelled_orders
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: _t("Shirt orders by size"),
    Component: PieChartCard,
    props: (data) => ({
        title: _t("Shirt orders by size"),
        values: data.orders_by_size,
    })
});
