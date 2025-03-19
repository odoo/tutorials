import { registry } from "@web/core/registry";

import { NumberCard } from "./cards/number_card";
import { PieChartCard } from "./cards/pie_chart_card";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        // size and props are optionals
        size: 3,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        }),
    },
    {
        id: "pie_chart_by_size",
        description: "Shirt orders by size",
        Component: PieChartCard,
        // size and props are optionals
        size: 3,
        props: (data) => ({
            title: "Shirt orders by size",
            label: "Size: ",
            data: data
        }),
    },
];

items.forEach((item) => registry.category("awesome_dashboard").add(item.id, item));

