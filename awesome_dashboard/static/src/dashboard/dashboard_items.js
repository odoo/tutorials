import { registry } from "@web/core/registry";

import { TextCard } from "./cards/text_card";
import { NumberCard } from "./cards/number_card";
import { PieChartCard } from "./cards/pie_chart_card";

const items = [
    // Text Cards
    {
        id: "normal_test",
        description: "Normal",
        Component: TextCard,
        // size and props are optionals
        props: (data) => ({
            title: "Normal",
            value: "I am normal hello",
        }),
    },
    {
        id: "big_test",
        description: "Big",
        Component: TextCard,
        // size and props are optionals
        size: 3.2, // Intervals between cards are 0.1
        props: (data) => ({
            title: "Big",
            value: "I am BIG yaaayyy",
        }),
    },

    // Number Cards
    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: "Total amount of new orders",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        // size and props are optionals
        props: (data) => ({
            title: "Average time for an order to go from \'new\' to \'sent\' or \'cancelled\'",
            value: data.average_time,
        }),
    },

    // Pie Chart Cards
    {
        id: "orders_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        // size and props are optionals
        size: 4,
        props: (stats) => ({
            title: "Shirt orders by size",
            label: "Shirt orders by size",
            data: stats.orders_by_size,
        }),
    },
];
 
items.forEach((item) => registry.category("awesome_dashboard").add(item.id, item));
