import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "new_orders",
        description: "Number of new Orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new Orders this month",
            value: data.nb_new_orders,
        })
    },
    {
        id: "total_amount",
        description: "Total Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total Number of new orders",
            value: data.total_amount,
        })
    },
    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.average_time,
        })
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt by order this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChartCard,
        props: (data) => ({
            title: "Shirt orders by size",
            values: data.orders_by_size,
        })
    }
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
