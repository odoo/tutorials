import { NumberCard } from "./numbercard/number_card";
import { PieChartCard } from "./piechartcard/piechart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export const items = [
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of tees ordered this month"),
            value: data.average_quantity,
        })
    },

    {
        id: "average_time",
        description: _t("Average time of an order"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            value: data.average_time,
        })
    },

    {
        id: "nb_new_orders",
        description: _t("Number of new orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders,
        })
    },

    {
        id: "nb_cancelled_orders",
        description: _t("Number of cancelled orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders,
        })
    },

    {
        id: "total_amount",
        description: _t("Total amount of new orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount,
        })
    },

    {
        id: "orders_pie_chart",
        description: _t("Shirt order by size"),
        Component: PieChartCard,
        props: (data) => ({
            title: _t("Shirt order by size"),
            data: data.orders_by_size,
        })
    },

]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
})

