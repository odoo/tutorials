import { InfoCard } from "../info_card/info_card";
import { PieChart } from "../pie_chart/pie_chart"
import { registry } from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: InfoCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
        enabled: true,
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: InfoCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
        enabled: true,
    },
    {
        id: "number_new_orders",
        description: "New orders this month",
        Component: InfoCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
        enabled: true,
    },
    {
        id: "cancelled_orders",
        description: "Cancelled orders this month",
        Component: InfoCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
        enabled: true,
    },
    {
        id: "amount_new_orders",
        description: "amount orders this month",
        Component: InfoCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
        enabled: true,
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChart,
        size: 1,
        props: (data) => ({
            label: "Shirt orders by size",
            data: data.orders_by_size
        }),
        enabled: true,
    }
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
