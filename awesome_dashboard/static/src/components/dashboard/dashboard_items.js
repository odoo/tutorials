/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { NumberCard } from "../number_card/number_card";
import { PieChartCard } from "../pie_chart_card/pie_chart_card";

const DASHBOARD_ITEMS = [
    {
        id: 'average_quantity',
        description: _lt("Average amount of t-shirt"),
        Component: NumberCard,
        props: (data) => ({
            title: _lt("Average amount of t-shirt by order this month"),
            value: data.average_quantity,
        }),
    },
    {
        id: 'average_time',
        description: _lt("Average flow time"),
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: _lt("Average time for an order to go from 'new' to 'sent' or 'canceled'"),
            value: data.average_time,
        }),
    },
    {
        id: 'nb_new_orders',
        description: _lt("New orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _lt("New orders this month"),
            value: data.nb_new_orders,
        }),
    },
    {
        id: 'nb_cancelled_orders',
        description: _lt("Cancelled orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _lt("Cancelled orders this month"),
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: 'total_amount',
        description: _lt("Total amount"),
        Component: NumberCard,
        props: (data) => ({
            title: _lt("Total amount"),
            value: data.total_amount,
        }),
    },
    {
        id: 'orders_by_size',
        description: _lt("Orders by Size"),
        Component: PieChartCard,
        props: (data) => {
            return ({
                title: _lt("Orders by Size"),
                data: {
                    datasets: [{
                        data: Object.values(data.orders_by_size)
                    }],
                    labels: Object.keys(data.orders_by_size),
                },
            });
        },
    },
];

for (const dashboardItem of DASHBOARD_ITEMS) {
    registry.category("awesome_dashboard").add(dashboardItem.id, dashboardItem);
}
