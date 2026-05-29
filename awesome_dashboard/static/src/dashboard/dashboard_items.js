import { registry } from "@web/core/registry"
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (statastics) => ({
            title: "Average amount of t-shirt by order this month",
            count: statastics.average_quantity,
        })
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        props: (statastics) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            count: statastics.average_time,
        })
    },
    {
        id: "number_new_orders",
        description: "New orders this month",
        Component: NumberCard,
        props: (statastics) => ({
            title: "Number of new orders this month",
            count: statastics.nb_new_orders,
        })
    },
    {
        id: "cancelled_orders",
        description: "Cancelled orders this month",
        Component: NumberCard,
        props: (statastics) => ({
            title: "Number of cancelled orders this month",
            count: statastics.nb_cancelled_orders,
        })
    },
    {
        id: "amount_new_orders",
        description: "amount orders this month",
        Component: NumberCard,
        props: (statastics) => ({
            title: "Total amount of new orders this month",
            count: statastics.total_amount,
        })
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (statastics) => ({
            title: "Shirt orders by size",
            labels: Object.keys(statastics.orders_by_size),
            datasets: [{ 'data': Object.values(statastics.orders_by_size) }]
        })
    },
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
