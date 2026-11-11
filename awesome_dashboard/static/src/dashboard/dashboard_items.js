import {NumberCard} from "./number_card/number_card";
import {PieChartCard} from "./piechart_card/piechart_card";
import {registry} from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average Quantity",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average Quantity",
            value: data.average_quantity,
            color: "primary",
        }),
    },
    {
        id: "average_time",
        description: "Average Time",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average Time",
            value: data.average_time,
            color: "info",
        }),
    },
    {
        id: "cancelled_orders",
        description: "Cancelled Orders",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Cancelled Orders",
            value: data.nb_cancelled_orders,
            color: "danger",
        }),
    },
    {
        id: "new_orders",
        description: "New Orders",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "New Orders",
            value: data.nb_new_orders,
            color: "success",
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders By Size",
        Component: PieChartCard,
        size: 3,
    },
    {
        id: "total_amount",
        description: "Total Amount",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Total Amount",
            value: data.total_amount,
            color: "primary",
        }),
    },
];


items.forEach((item) => registry.category("awesome_dashboard").add(item.id, item));