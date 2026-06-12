/** @odoo-module **/
import { dashboardItemRegistry } from "./dashboard_registry";
import { NumberCard }   from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { _t } from "@web/core/l10n/translation";

dashboardItemRegistry.add("new_orders", {
    id: "new_orders",
    description: _t("New orders this month"),
    Component: NumberCard,
    size:  1,
    props: (data) => ({
        title: _t("Number of new orders"),
        value: data?.nb_new_orders || 0,
    }),
});

dashboardItemRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total amount orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Total amount"),
        value: data?.total_amount || 0,
    }),
});

dashboardItemRegistry.add("avg_quantity", {
    id: "avg_quantity",
    description: _t("Average amount of t-shirt"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average quantity"),
        value: data?.average_quantity || 0,
    }),
});

dashboardItemRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average time new to sent/cancelled"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average time"),
        value: data?.average_time || 0,
    }),
});

dashboardItemRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Cancelled orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Number of cancelled orders"),
        value: data?.nb_cancelled_orders || 0,
    }),
});

dashboardItemRegistry.add("pie_chart", {
    id:  "pie_chart",
    description: _t("Shirt orders by size"),
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: _t("Orders by size"),
        data:  data?.orders_by_size || {},
    }),
});
