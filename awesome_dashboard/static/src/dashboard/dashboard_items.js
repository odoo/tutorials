import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { NumberCard } from "./number_card/number_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

const items = [
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            value: data.average_time,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by Size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Orders by Size"),
            value: data.orders_by_size,
        }),
    },
];

items.forEach((item) => registry.category("awesome_dashboard").add(item.id, item));
