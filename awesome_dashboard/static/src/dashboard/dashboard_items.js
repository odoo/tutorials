import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";

export const items = [
    {
        id: "average_quantity",
        description: "Average quantity",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirts by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "average_time",
        description: "Average time",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        }),
    },
    {
        id: "nb_new_orders",
        description: "Number of new orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total orders",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "tshirt_sizes",
        description: "T-Shirt orders chart",
        Component: PieChartCard,
        size: 1,
        props: (data) => ({
            title: "T-Shirt Sizes By Amount Sold",
            data: data.orders_by_size,
        }),
    },
];

registry.category("awesome_dashboard").add("DashboardItems", items);
