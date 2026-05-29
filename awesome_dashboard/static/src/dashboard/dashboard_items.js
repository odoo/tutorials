import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: _t("Number of new orders this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total amount of new orders this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount,
    }),
});

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average amount of t-shirt by order this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Number of cancelled orders this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average time for an order"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.average_time,
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: _t("Shirt orders by size"),
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: _t("Shirt orders by size"),
        data: data.orders_by_size,
    }),
});
