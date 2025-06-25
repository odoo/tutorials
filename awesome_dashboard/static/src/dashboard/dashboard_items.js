import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

const items = [
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: _t("Average time for an order"),
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            value: data.average_time,
        }),
    },
    {
        id: "number_new_orders",
        description: _t("New orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: _t("Cancelled orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: _t("Amount of orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount,
        }),
    },
    {
        id: "pie_chart",
        description: _t("Shirt orders by size"),
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Shirt orders by size"),
            data: data.orders_by_size,
        }),
    },
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
})
