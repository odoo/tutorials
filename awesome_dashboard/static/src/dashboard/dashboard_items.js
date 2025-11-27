import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { _t } from "@web/core/l10n/translation";

const dashboardItems = registry.category("awesome_dashboard");

dashboardItems.add("average_quantity", {
    description: _t("Average amount of t-shirt"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity,
    }),
});

dashboardItems.add("average_time", {
    description: _t("Average time for an order"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.average_time,
    }),
});

dashboardItems.add("nb_new_orders", {
    description: _t("Number of new orders"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders,
    }),
});

dashboardItems.add("nb_cancelled_orders", {
    description: _t("Number of cancelled orders"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardItems.add("total_amount", {
    description: _t("Total amount of new orders"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount,
    }),
});

dashboardItems.add("orders_by_size", {
    description: _t("Orders by size"),
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: _t("Orders by size"),
        data: data.orders_by_size,
    }),
});
