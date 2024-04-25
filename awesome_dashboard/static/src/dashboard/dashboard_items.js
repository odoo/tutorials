/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { _t } from "@web/core/l10n/translation";

const average_quantity = {
    id: "average_quantity",
    description: _t("Average amount of t-shirt"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity
    }),
}
registry.category("awesome_dashboard").add("average_quantity", average_quantity);

const nb_new_orders = {
    id: "nb_new_orders",
    description: _t("Number of new orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders
    }),
}
registry.category("awesome_dashboard").add("nb_new_orders", nb_new_orders);

const total_amount = {
    id: "total_amount",
    description: _t("Total amount of new orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount
    }),
}
registry.category("awesome_dashboard").add("total_amount", total_amount);

const nb_cancelled_orders = {
    id: "nb_cancelled_orders",
    description: _t("Number of cancelled orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.nb_cancelled_orders
    }),
}
registry.category("awesome_dashboard").add("nb_cancelled_orders", nb_cancelled_orders);

const average_time = {
    id: "average_time",
    description: _t("Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’"),
        value: data.average_time
    }),
}
registry.category("awesome_dashboard").add("average_time", average_time);

const orders_by_size = {
        id: "orders_by_size",
        description: _t("Chart of sizes"),
        Component: PieChartCard,
        size: 1,
        props: (data) => ({
            title: _t("Chart of sizes"),
            value: data.orders_by_size
        }),
    }
registry.category("awesome_dashboard").add("orders_by_size", orders_by_size);
