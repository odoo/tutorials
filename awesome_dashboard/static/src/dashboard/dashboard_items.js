/** @odoo-module **/

import { PieChartCard } from "../pie_chart_card/pie_chart_card";
import { NumberCard } from "../number_card/number_card";

export const items = [
    {
        id: 0,
        size: 1.5,
        Component: NumberCard,
        title: 'Average amount of t-shirt by order this month',
        extract: (data) => ({
            value: data.average_quantity,
        }),
    },
    {
        id: 1,
        size: 2,
        Component: NumberCard,
        title: 'Average time for an order to go from "new" to "sent" or "cancelled"',
        extract: (data) => ({
            value: data.average_time,
        }),
    },
    {
        id: 2,
        size: 1,
        Component: NumberCard,
        title: 'Number of new orders this month',
        extract: (data) => ({
            value: data.nb_new_orders,
        }),
    },
    {
        id: 3,
        size: 1,
        Component: NumberCard,
        title: 'Number of cancelled orders this month',
        extract: (data) => ({
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: 4,
        Component: NumberCard,
        title: 'Total amount of new orders this month',
        extract: (data) => ({
            value: data.total_amount,
        }),
    },
    {
        id: 5,
        Component: PieChartCard,
        title: 'Shirt orders by size',
        extract: (data) => ({
            value: data.orders_by_size,
        }),
    },
];
