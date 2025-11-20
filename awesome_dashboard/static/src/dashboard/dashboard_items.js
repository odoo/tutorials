/** @odoo-module **/

import { dashboardRegistry } from "./dashboard_registry";
import { NumberCard } from "./number_card/number_card";
import { PieChart } from "./pie_chart/pie_chart";

// Define dashboard items and register them
dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average T-Shirts per Order",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Avg. T-Shirts per Order",
        value: data.average_quantity
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average Order Processing Time",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Avg. Processing Time",
        value: data.average_time + " hrs"
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "New Orders This Month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Sales Amount",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: "Total Sales",
        value: "$" + data.total_amount
    }),
});


dashboardRegistry.add("order_size_distribution", {
    id: "order_size_distribution",
    description: "T-Shirt Size Distribution",
    Component: PieChart,
    size: 2,
    props: (data) => ({
        sizes: Object.keys(data.orders_by_size),
        quantities: Object.values(data.orders_by_size)
    }),
});
