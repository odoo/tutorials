/** @odoo-module */

import { registry } from "@web/core/registry";
import { NumberCard } from "./components/number_card/number_card";
import { PieChartCard } from "./components/pie_chart_card/pie_chart_card";

// create registry category
const dashboardItemsRegistry = registry.category("awesome_dashboard.items");

// ✅ Register items one by one

dashboardItemsRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "New Orders",
    Component: NumberCard,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
    }),
});

dashboardItemsRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    props: (data) => ({
        title: "Total Amount",
        value: data.total_amount,
    }),
});

dashboardItemsRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Avg Quantity",
    Component: NumberCard,
    props: (data) => ({
        title: "Avg T-Shirts / Order",
        value: data.average_quantity,
    }),
});

dashboardItemsRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders,
    }),
});

dashboardItemsRegistry.add("average_time", {
    id: "average_time",
    description: "Avg Time",
    Component: NumberCard,
    props: (data) => ({
        title: "Avg Processing Time",
        value: data.average_time,
    }),
});

dashboardItemsRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "T-Shirt Sizes",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "T-Shirt Sizes",
        data: data.orders_by_size,
    }),
});