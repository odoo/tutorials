import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { registry } from '@web/core/registry';

const dashboardItems = [
    {
        id: 'average_quantity',
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.stats.average_quantity
        }),
    },
    {
        id: 'average_time',
        description: "",
        Component: NumberCard,
        size: 3,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.stats.average_time
        }),
    },
    {
        id: 'nb_new_orders',
        description: "",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.stats.nb_new_orders
        }),
    },
    {
        id: 'nb_cancelled_orders',
        description: "",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.stats.nb_cancelled_orders
        }),
    },
    {
        id: 'total_amount',
        description: "",
        Component: NumberCard,
        props: (data) => ({
            title: "Total number of new orders this month",
            value: data.stats.total_amount
        }),
    },
    {
        id: 'pie_chart',
        description: "",
        size: 2,
        Component: PieChartCard,
        props: (data) => ({
            title: "Shirt orders by size"
        })
    }
];

const dashboardRegistry = registry.category('awesome_dashboard');
for (const item of dashboardItems) {
    dashboardRegistry.add(item.id, item);
}
