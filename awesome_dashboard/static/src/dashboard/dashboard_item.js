import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";


export const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirts",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Avg. T-Shirts per Order",
            value: data.average_quantity,
        }),
    },
    {
        id: "sales_distribution",
        description: "Sales distribution per size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            data: data.orders_by_size,
        }),
    }
];
