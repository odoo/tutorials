
import { NumberCard } from "./number_card/number_card.js";
import { PieChartCard } from "./pie_chart_card/pie_chart_card.js";
import { dashboardItemRegistry } from "./dashboard_registry";
import { _t } from "@web/core/l10n/translation";

dashboardItemRegistry.add("new_orders", {
    id: "new_orders",
    description: "New Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "New Orders",
        value: data?.nb_new_orders || 0,
    }),
});

dashboardItemRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Amount",
        value: data?.total_amount || 0,
    }),
});

dashboardItemRegistry.add("avg_quantity", {
    id: "avg_quantity",
    description: "Average Quantity",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average Quantity",
        value: data?.average_quantity || 0,
    }),
});

dashboardItemRegistry.add("pie_chart", {
    id: "pie_chart",
    description: "Orders by Size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "Orders by Size",
        data: data?.orders_by_size || {},
    }),
});