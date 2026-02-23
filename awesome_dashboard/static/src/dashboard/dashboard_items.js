import { registry } from "@web/core/registry";
import { NumberCard } from "./components/number_card/number_card";
import { PieChart } from "./components/pie_chart/pie_chart";

const awesomeDashboardRegistry = registry.category("awesome_dashboard");

const items = [
    {
        id: "average_quantity",
        description: "Average Quantity",
        Component: NumberCard,
        props: (data) => ({
            title: "Average Quantity",
            value: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: "Average Time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average Time",
            value: data.average_time
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Cancelled Orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Cancelled Orders",
            value: data.nb_cancelled_orders
        }),
    },
    {
        id: "nb_new_orders",
        description: "New Orders",
        Component: NumberCard,
        props: (data) => ({
            title: "New Orders",
            value: data.nb_new_orders
        }),
    },
    {
        id: "total_amount",
        description: "Total Amount",
        Component: NumberCard,
        props: (data) => ({
            title: "Total Amount",
            value: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: "Orders by Size",
        Component: PieChart,
        size: 2,
        props: (data) => ({
            title: "Orders by Size",
            ordersBySize: data.orders_by_size
        }),
    },
];

items.forEach(item => {
    awesomeDashboardRegistry.add(item.id, item);
});