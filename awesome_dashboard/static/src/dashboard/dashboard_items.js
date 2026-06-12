// static/src/dashboard/dashboard_items.js

import { registry } from "@web/core/registry";
import { NumberCard } from "./components/number_card/number_card";
import { PieChartCard } from "./components/pie_chart/piechart";
import { _t } from "@web/core/l10n/translation";

const dashboardRegistry = registry.category("awesome_dashboard");
dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average quantity of t-shirts"),
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average time for an order"),
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: _t("Average time to complete an order (days)"),
        value: data.average_time,
    }),
});

dashboardRegistry.add("num_new_orders", {
    id: "num_new_orders",
    description: _t("Number of new orders this month"),
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: _t("New orders this month"),
        value: data.num_new_orders,
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: _t("Orders by t-shirt size"),
    Component: PieChartCard,
    size: 3,
    props: (data) => ({
        labels: Object.keys(data.orders_by_size),
        values: Object.values(data.orders_by_size),
        title: _t("Orders by size"),
    }),
});