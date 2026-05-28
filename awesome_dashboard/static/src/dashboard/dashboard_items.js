import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: _t("New Orders This Month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("New Orders This Month"),
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total Amount New Orders"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total Amount New Orders"),
        value: data.total_amount,
    }),
});

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average T-Shirts Per Order"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average T-Shirts Per Order"),
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Cancelled Orders"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Cancelled Orders"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Avg Time New to Sent/Cancelled"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Avg Time New to Sent/Cancelled"),
        value: data.average_time,
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: _t("T-Shirts Sold by Size"),
    Component: PieChartCard,
    size: 3,
    props: (data) => ({
        data: data.orders_by_size,
    }),
});
