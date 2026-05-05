import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export let items = [
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt"),
        Component: NumberCard,
        // size and props are optionals
        size: 3,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: _t("Average time for an order"),
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: _t("Average time for an order to go from new to sent or canceled"),
            value: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: _t("New orders this month"),
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders
        }),
    }, {
        id: "nb_cancelled_orders",
        description: _t("Canceled orders this month"),
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: _t("Number of canceled orders this month"),
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_amount",
        description: _t("Amount of orders this month"),
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: _t("Total amount of orders this month"),
            value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: _t("Shirt orders by size"),
        Component: PieChartCard,
        // size and props are optionals
        props: (data) => ({
            title: _t("Shirt orders by size"),
            values: data.orders_by_size
        }),
    },

];

items.forEach(item => registry.category("awesome_dashboard").add(item.id, item));
