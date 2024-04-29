/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { NumberCard } from "./number_card/number_card"
import { PieChartCard } from "./pie_chart_card/pie_chart_card"


const dashboardItems = [
    {
        id: "nb_new_orders",
        description: _t("Number of new orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders
        }),
    },
    {
        id: "total_amount",
        description: _t("Total amount of new orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount
        }),
    },
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: _t("Number of cancelled orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "average_time",
        description: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            value: data.average_time
        }),
    },
    {
        id: "pie_char",
        description: _t("Pie chart with the Order amount by size"),
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Pie chart with the Order amount by size"),
            value: data.orders_by_size
        }),
    },
]

dashboardItems.forEach((item) => (
    registry.category("awesome_dashboard").add(item.id, item)
))