/** @odoo-module **/
import { dashboardRegistry } from "@awesome_dashboard/dashboard/dashboard_registry";
import { NumberCard } from "@awesome_dashboard/dashboard/numbercard";
import { PieChartCard } from "@awesome_dashboard/dashboard/piechartcard";

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average T-Shirts Sold",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month:",
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average Time",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled':",
        value: data.average_time,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "new orders",
    Component: NumberCard,
    size: 1.3,
    props: (data) => ({
        title: "Number of new orders this month:",
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "cencelled orders",
    Component: NumberCard,
    size: 1.3,
    props: (data) => ({
        title: "Number of cancelled orders this month:",
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "total amount",
    Component: NumberCard,
    size: 1.3,
    props: (data) => ({
        title: "Total amount of new orders this month:",
        value: data.total_amount,
    }),
});

dashboardRegistry.add("sales_distribution", {
    id: "sales_distribution",
    description: "Sales by Size",
    Component: PieChartCard,
    size: 1,
    props: (data) => ({
        labels: Object.keys(data.orders_by_size),
        data: Object.values(data.orders_by_size),
    }),
});
