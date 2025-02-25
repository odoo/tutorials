import { Component } from "@odoo/owl";
import { dashboardRegistry } from "../dashboard_registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static defaultProps = {
        size: 1,
    };
}

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.avgQuantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average time for order processing",
    Component: NumberCard,
    size: 3,
    props: (data) => ({
        title: "Average time for an order to go 'new' to 'sent' or 'cancelled'",
        value: data.avgTime,
    }),
});

dashboardRegistry.add("new_orders", {
    id: "new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.newOrders,
    }),
});

dashboardRegistry.add("cancelled_orders", {
    id: "cancelled_orders",
    description: "Number of cancelled orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.cancelledOrders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.totalAmount
    }),
});

dashboardRegistry.add("order_distribution", {
    id: "order_distribution",
    description: "Order Distribution Pie Chart",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        labels: ["s", "xl", "l"],
        values: [40, 30, 30],
    }),
});
