import { registry } from "@web/core/registry"
import { NumberCard } from "./components/number_card/number_card";
import { PieChart } from "./components/pie_chart/pie_chart";
import { _t } from "@web/core/l10n/translation";

const dashboardRegistry = registry.category("awesome_dashboard.items");


dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average amount of t-shirt"),
    component: NumberCard,
    size: 2,
    props: (data) => ({
        label: _t("Average Quantity"),
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average order processing time"),
    component: NumberCard,
    size: 2,
    props: (data) => ({
        label: _t("Average time"),
        value: data.average_time,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: _t("New orders this month"),
    component: NumberCard,
    size: 1,
    props: (data) => ({
        label: _t("New orders this month"),
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Cancelled orders this month"),
    component: NumberCard,
    size: 1,
    props: (data) => ({
        label: _t("Number of Cancelled Orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total sales amount"),
    component: NumberCard,
    size: 1,
    props: (data) => ({
        label: _t("Total amount of new Orders This Month"),
        value: data.total_amount,
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: _t("Shirt orders by size"),
    component: PieChart,
    size: 2,
    props: (data) => ({
        label: _t("Shirt orders by size"),
        data: data.orders_by_size,
    }),
});