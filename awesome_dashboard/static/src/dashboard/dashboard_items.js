/** @odoo-module **/

import { NumberCard } from '../number_card/number_card';
import { PieChartCard } from '../pie_chart_card/pie_chart_card';
import { registry } from '@web/core/registry';
import { _t } from '@web/core/l10n/translation';

const dashboardRegistry = registry.category('awesome_dashboard');

dashboardRegistry.add('average_quantity', {
    id: 'avg_qty',
    description: "Average amount of t-shirt",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.qty_avg,
    }),
});

dashboardRegistry.add('average_time', {
    id: 'avg_time',
    description: "Average time for an order",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.time_avg,
    }),
});

dashboardRegistry.add('number_new_orders', {
    id: 'new_orders',
    description: "New orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.orders_new,
    }),
});

dashboardRegistry.add('cancelled_orders', {
    id: 'cxl_orders',
    description: "Cancelled orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.orders_cancelled,
    }),
});

dashboardRegistry.add('amount_new_orders', {
    id: 'amount_orders',
    description: "Amount orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.amount_total,
    }),
});

dashboardRegistry.add('pie_chart', {
    id: 'size_chart',
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: _t("Shirt orders by size"),
        values: data.sizes_orders,
    }),
});
