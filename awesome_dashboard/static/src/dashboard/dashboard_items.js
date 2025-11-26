/** @odoo-module **/

import {registry} from "@web/core/registry"
import { NumberCard } from "./components/number_card/number_card";
import { PieChartCard } from "./components/piechart_card/piechart_card";

const dashboardRegistry = registry.category("awesome_dashboard")

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of T-shirts per order",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average T-Shirts per Order",
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("processing_time", {
    id: "processing_time",
    description: "Average Processing Time",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average Processing Time",
        value: data.average_time,
    }),
});

dashboardRegistry.add("new_orders", {
    id: "new_orders",
    description: "New Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Cancelled Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Amount",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Amount",
        value: data.total_amount,
    }),
});

dashboardRegistry.add("size_distribution", {
    id: "size_distribution",
    description: "Size Distribution",
    Component: PieChartCard,
    size: 2,
    props: (data) => {
        console.log("Dashboard data:", data);
        return {
            title:"Size Distribution",
            sizes: Object.keys(data.orders_by_size || {}), 
            quantities: Object.values(data.orders_by_size || {}),
        };
    },  
});

dashboardRegistry.add("orders_distribution", {
    id: "orders_distribution",
    description: "Orders Distribution",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title:"Orders Distribution",
        sizes: ["New Orders", "Cancelled Orders"],
        quantities: [data.nb_new_orders, data.nb_cancelled_orders],
    }),
});
