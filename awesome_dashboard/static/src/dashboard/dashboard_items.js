import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

const dashboardItems = registry.category("awesome_dashboard");

dashboardItems.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity,
    }),
});

dashboardItems.add("average_time", {
    id: "average_time",
    description: "Average time for an order",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.average_time,
    }),
});

dashboardItems.add("number_new_orders", {
    id: "number_new_orders",
    description: "New orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders,
    }),
});

dashboardItems.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardItems.add("amount_new_orders", {
    id: "amount_new_orders",
    description: "Amount orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount,
    }),
});

dashboardItems.add("pie_chart", {
    id: "pie_chart",
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: _t("Shirt orders by size"),
        data: data.orders_by_size,
    }),
});
