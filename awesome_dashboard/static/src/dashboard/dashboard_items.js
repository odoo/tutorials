import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average number of t-shirt by order",
        Component: NumberCard,
        props: (data) => ({
            title: "Average number of t-shirt by order",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        props: (data) =>({
            title: "Average time for an order to go from 'new' to 'send' or 'cancelled'",
            value: data.average_time,
        }),
        size: 2,
    },
    {
        id: "number_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) =>({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "number_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) =>({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_order",
        description: "Total amount of orders",
        Component: NumberCard,
        props: (data) =>({
            title: "Total amount of orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by size",
        Component: PieChartCard,
        props: (data) =>({
            title: "Shirt orders by size",
            data: data['orders_by_size'],
        }),
        size: 2,
    },

];

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
