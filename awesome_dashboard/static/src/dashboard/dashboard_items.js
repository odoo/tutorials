import { dashboardItemRegistry } from "./dashboard_registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { _t } from "@web/core/l10n/translation";

dashboardItemRegistry.add("new_orders", {
    id: "new_orders",
    description: _t("Average amount of t-shirt"), 
    component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Number of new orders",
        value: data?.nb_new_orders || 0,
    }),
});

dashboardItemRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Average amount of t-shirt"), 
    component: NumberCard,
    props: (data) => ({
        title: "Total amount",
        value: data?.total_amount || 0,
    }),
});

dashboardItemRegistry.add("avg_quantity", {
    id: "avg_quantity",
    description: _t("Average amount of t-shirt"), 
    component: NumberCard,
    props: (data) => ({
        title: "Average quantity",
        value: data?.average_quantity || 0,
    }),
});

dashboardItemRegistry.add("pie_chart", {
    id: "pie_chart",
    description: _t("Average amount of t-shirt"), 
    component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "Orders by size",
        data: data?.orders_by_size || 0,
    }),
});
