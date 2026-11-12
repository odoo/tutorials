import {NumberCard} from "./number_card/number_card";
import {PieChartCard} from "./piechart_card/piechart_card";
import {registry} from "@web/core/registry";
import {_t} from "@web/core/l10n/translation";

const items = [
    {
        id: "average_quantity",
        description: _t("Average Quantity"),
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: _t("Average Quantity"),
            value: data.average_quantity,
            color: "primary",
        }),
    },
    {
        id: "average_time",
        description: _t("Average Time"),
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: _t("Average Time"),
            value: data.average_time,
            color: "info",
        }),
    },
    {
        id: "cancelled_orders",
        description: _t("Cancelled Orders"),
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: _t("Cancelled Orders"),
            value: data.nb_cancelled_orders,
            color: "danger",
        }),
    },
    {
        id: "new_orders",
        description: _t("New Orders"),
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: _t("New Orders"),
            value: data.nb_new_orders,
            color: "success",
        }),
    },
    {
        id: "orders_by_size",
        description: _t("Orders By Size"),
        Component: PieChartCard,
        size: 3,
    },
    {
        id: "total_amount",
        description: _t("Total Amount"),
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: _t("Total Amount"),
            value: data.total_amount,
            color: "primary",
        }),
    },
];

items.forEach((item) =>
    registry.category("awesome_dashboard").add(item.id, item)
);
