import { NumberCard } from "./number_card/number_card";
import { ChartCard } from "./chart_card/chart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export const items = [
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
        id: "average_time",
        description: "Average time for order",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' of 'cancelled'"),
            value: data.average_time,
        }),
    },
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
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: ChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Shirt orders by size"),
            value: data['orders_by_size'],
            type: "pie"
        }),
    },
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
