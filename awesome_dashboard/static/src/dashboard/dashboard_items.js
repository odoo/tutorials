/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { NumberCard } from "./cards/number_card";
import { PieChartCard } from "./cards/pie_chart_card";

const awesomeDash = registry.category("awesome_dashboard");

awesomeDash.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average amount of t-shirt"),
    Component: NumberCard,
    size: 1,
    props: (statistics) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: statistics.value.average_quantity,
    }),
});

awesomeDash.add("average_time", {
    id: "average_time",
    description: _t("Average time for an order"),
    Component: NumberCard,
    props: (statistics) => ({
        title: _t("Average time for an order to go from 'New' to 'Sent' or 'Cancelled'"),
        value: statistics.value.average_time,
    }),
});

awesomeDash.add("nb_new_orders", {
    id: "nb_new_orders",
    description: _t("Number of new orders this month"),
    Component: NumberCard,
    props: (statistics) => ({
        title: _t("Number of new orders this month"),
        value: statistics.value.nb_new_orders,
    }),
});

awesomeDash.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Number of cancelled orders this month"),
    Component: NumberCard,
    props: (statistics) => ({
        title: _t("Number of cancelled orders this month"),
        value: statistics.value.nb_cancelled_orders,
    }),
});

awesomeDash.add("total_amount", {
    id: "total_amount",
    description: _t("Total amount of new orders this month"),
    Component: NumberCard,
    props: (statistics) => ({
        title: _t("Total amount of new orders this month"),
        value: statistics.value.total_amount,
    }),
});

awesomeDash.add("orders_by_size", {
    id: "orders_by_size",
    description: _t("Shirt orders by size"),
    Component: PieChartCard,
    size: 2,
    props: (statistics) => ({
        title: _t("Shirt orders by size"),
        data: statistics.value.orders_by_size,
    }),
});
