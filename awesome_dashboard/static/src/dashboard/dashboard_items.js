import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { NumberCard, PieChartCard } from "./dashboard_components";

const dashboardItemRegistry = registry.category("awesome_dashboard.items");

dashboardItemRegistry.add("new_orders", {
    id: "new_orders",
    description: "New Orders",
    Component: NumberCard,
    size: 1,
    props: (data = {}) => ({
        title: _t("New Orders"),
        value: data.nb_new_orders || 0,
    }),
});

dashboardItemRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    size: 1,
    props: (data = {}) => ({
        title: _t("Total Amount"),
        value: data.total_amount || 0,
    }),
});

dashboardItemRegistry.add("avg_quantity", {
    id: "avg_quantity",
    description: "Average Quantity",
    Component: NumberCard,
    size: 1,
    props: (data = {}) => ({
        title: _t("Avg T-Shirts / Order"),
        value: data.average_quantity || 0,
    }),
});

dashboardItemRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 1,
    props: (data = {}) => ({
        title: _t("Cancelled Orders"),
        value: data.nb_cancelled_orders || 0,
    }),
});

dashboardItemRegistry.add("pie_chart", {
    id: "pie_chart",
    description: "Orders by Size",
    Component: PieChartCard,
    size: 2,
    props: (data = {}) => ({
        title: _t("Orders by Size"),
        data: data.orders_by_size || {},
    }),
});
