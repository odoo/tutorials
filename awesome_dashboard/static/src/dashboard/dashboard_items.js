/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./components/number_card";
import { PieChartCard } from "./components/pie_chart_card";

// Create a new registry category for dashboard items
const itemRegistry = registry.category("awesome_dashboard_items");

itemRegistry.add("new_orders", {
    id: "new_orders",
    description: "New Orders This Month",
    Component: NumberCard,
    props: (data) => ({
        title: "New Orders This Month",
        value: data.nb_new_orders || 0,
    }),
});

itemRegistry.add("revenue", {
    id: "revenue",
    description: "Total Revenue This Month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Revenue This Month",
        value: data.total_amount?.toFixed(2) || "0.00",
    }),
});

itemRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Avg. T-Shirts per Order",
    Component: NumberCard,
    props: (data) => ({
        title: "Avg. T-Shirts per Order",
        value: data.average_quantity || 0,
    }),
});

itemRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders || 0,
    }),
});

itemRegistry.add("average_time", {
    id: "average_time",
    description: "Avg. Time New → Sent/Cancelled",
    Component: NumberCard,
    props: (data) => ({
        title: "Avg. Time to Resolution (hrs)",
        value: data.average_time || 0,
    }),
});

itemRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Orders by Size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        data: data.orders_by_size || {},
    }),
});
