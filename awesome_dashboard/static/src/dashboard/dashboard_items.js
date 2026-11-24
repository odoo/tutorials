import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card";

const dashboardRegistry = registry.category("awesome_dashboard");
console.log(dashboardRegistry);


dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total Orders"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Orders",
        value: data.total_amount,
    }),
});

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average Quantity",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average Quantity",
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average Time",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average Time",
        value: data.average_time,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "New Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("sales_by_size", {
    id: "sales_by_size",
    description: "Sales by T-shirt Size",
    Component: PieChartCard,
    size: 3,
    props: (data) => ({
        title: "Sales by T-shirt Size",
        labels: data.qty_by_size.labels,
        values: data.qty_by_size.values,
    }),
});
