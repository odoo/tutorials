import { Component } from "@odoo/owl";
import { NumberCard, PieChartCard } from "./../card/card";
import { registry } from "@web/core/registry";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: { type: Number, optional: true },
        slots: {
            type: Object,
            shape: {
                default: Object,
            },
        },
    };
    static defaultProps = {
        size: 1,
    };
}

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average quantity per order",
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: "Average time",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average Time",
        value: data.average_time,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Cancelled orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Cancelled Orders",
        value: data.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "New orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "New Orders",
        value: data.nb_new_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Amount",
        value: `${data.total_amount} €`, 
    }),
});

dashboardRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: "T-Shirt Sizes",
        data: data.orders_by_size,
    }),
});