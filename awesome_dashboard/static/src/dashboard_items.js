/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./dashboard/components/number_card";
import { PieChartCard } from "./dashboard/components/pie_chart_card";

const awesomeDashboardRegistry = registry.category("awesome_dashboard_items");

awesomeDashboardRegistry.add("new_orders", {
    id: "new_orders",
    description: "New Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.new_orders,
    }),
});

awesomeDashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
    }),
});

awesomeDashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average Quantity",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average amount of t-shirts per order",
        value: data.average_quantity,
    }),
});

awesomeDashboardRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.cancelled_orders,
    }),
});

awesomeDashboardRegistry.add("avg_order_time", {
    id: "avg_order_time",
    description: "Average Order Time",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Average time from ‘new’ to ‘sent’ or ‘cancelled’",
        value: data.avg_order_time,
    }),
});

awesomeDashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Order Distribution",
    Component: PieChartCard,
    size: 2,
        props: (data) => ({
            title: "Distribution of T-Shirt Sizes Sold",
            data: data.orders_by_size,
        }),
});
