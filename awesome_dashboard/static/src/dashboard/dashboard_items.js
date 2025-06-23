import { NumberCard } from "./numberCard/number_card";
import { PieChartCard } from "./pieChartCard/pie_chart_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "nb_new_orders",
        description: "The number of new orders, this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "New Orders This Month:",
            value: data.data.nb_new_orders
        }),
    },
    {
        id: "total_amount",
        description: "The total amount of orders, this month",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Total Amount This Month:",
            value: data.data.total_amount
        }),
    },
    {
        id: "average_quantity",
        description: "The average number of t-shirts by order",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Avg. T-Shirts per Order:",
            value: data.data.average_quantity
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "The number of cancelled orders, this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Cancelled Orders:",
            value: data.data.nb_cancelled_orders
        }),
    },
    {
        id: "average_time",
        description: "The average time (in hours) elapsed between the moment an order is created, and the moment is it sent",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Avg. Time New → Sent/Cancelled:",
            value: data.data.average_time
        }),
    },
    {
        id: "orders_by_size",
        description: "Number of shirts ordered based on size",
        Component: PieChartCard,
        size: 3,
        props: (data) => ({
            title: "Shirt orders by size:",
            value: data.data.orders_by_size
        }),
    }
]
items.forEach((item) => {
    registry.category("awesome_dashboard").add(item.id, item)
});
