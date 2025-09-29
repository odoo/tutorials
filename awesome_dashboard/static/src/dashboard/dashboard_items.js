import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const items = [
    {
        id: "average_quantity",
        description: _t("Average amount"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: _t("Average Time"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average Time"),
            value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: _t("Number of new orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders"),
            value: data.nb_new_orders
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: _t("Number of cancelled orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders"),
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_amount",
        description: _t("Total amount"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount"),
            value: data.total_amount
        }),
    },
    {
        id: "pie_chart",
        description: _t("Shirts orders by size"),
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Shirts orders by size"),
            value: data.orders_by_size
        }),
    },
]

items.forEach((item => {
    registry.category("awesome_dashboard.items").add(item.id, item);
}));
