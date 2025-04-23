/** @odoo-module **/
import { registry } from "@web/core/registry"
import { NumberCard } from "./components/NumberCard";
import { PieChartCard } from "./components/PieChartCard";
import { _t } from "@web/core/l10n/translation";

const dashboardRegistry = registry.category("awesome_dashboard.items");

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average amount of t-shirt"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average amount of T-Shirts by this month"),
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average order processing time"),
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.average_time,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: _t("New orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Cancelled orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Number of Cancelled Orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total sales amount"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Total amount of new Orders This Month"),
        value: data.total_amount,
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
