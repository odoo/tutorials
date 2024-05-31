/** @odoo-module **/
import { StatCard } from "./stat_card/stat_card";
import { PieChart } from "./pie_chart/pie_chart";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "1",
        description: "Average amount of t-shirt",
        Component: StatCard,
        props: (statistics) => ({
            title: "Average amount of t-shirt by order this month",
            data: statistics.average_quantity
        }),
    },
    {
        id: "2",
        description: "Average time elapsed by order",
        Component: StatCard,
        props: (statistics) => ({
            title: "the average time (in hours) elapsed between the moment an order is created, and the moment is it sent",
            data: statistics.average_time
        }),
    },
    {
        id: "3",
        description: "Number of cancelled order",
        Component: StatCard,
        props: (statistics) => ({
            title: "the number of cancelled orders, this month",
            data: statistics.nb_cancelled_orders
        }),
    },
    {
        id: "4",
        description: "total number of orders",
        Component: StatCard,
        props: (statistics) => ({
            title: "the total amount of orders, this month",
            data: statistics.total_amount
        }),
    },
    {
        id: "5",
        description: "Shirt orders by size",
        Component: PieChart,
        props: (statistics) => ({
            data: statistics.orders_by_size
        }),
    }
];

registry.category("awesome_dashboard").add("items", items);

