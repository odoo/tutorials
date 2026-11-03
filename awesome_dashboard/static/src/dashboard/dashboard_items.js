import { Registry, Component, types as t } from "@odoo/owl";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export const items = new Registry({
  name: "awesome_dashboard",
  validation: t.object({
    id: t.string(),
    description: t.string(),
    Component: t.constructor(Component),
    size: t.number().optional(),
    props: t.function().optional(),
  }),
});

const itemsList = [
    {
        id: "nb_new_orders",
        description: "New orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "New orders",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Total amount",
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled orders",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Cancelled orders",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average processing time",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Average processing time",
            value: data.average_time,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by size",
        Component: PieChartCard,
        size: 1,
        props: (data) => ({
            title: "Orders by size",
            values: Object.values(data.orders_by_size),
            labels: Object.keys(data.orders_by_size),
        }),
    },
];

itemsList.forEach((item) => items.addById(item));