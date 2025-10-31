import { Component } from "@odoo/owl";
import { PieChart } from "./piechart/piechart";
import { NumberCard } from "./numbercard/numbercard";
import { PieChartCard } from "./piechartcard/piechartcard";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";


const dashboardItemsRegistry = registry.category("awesome_dashboard");

dashboardItemsRegistry.add("average_quantity", {
    backend_attribute: "average_quantity",
    description: "Average amout of t-shirt",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity,
    })
});

dashboardItemsRegistry.add("average_time", {
    backend_attribute: "average_time",
    description: "Average time for an order",
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.average_time,
    }),
});

dashboardItemsRegistry.add("nb_new_orders", {
    backend_attribute: "nb_new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders,
    }),
});

dashboardItemsRegistry.add("nb_cancelled_orders", {
    backend_attribute: "nb_cancelled_orders",
    description: "Number of cancelled orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

dashboardItemsRegistry.add("total_amount", {
    backend_attribute: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount,
    }),
});

dashboardItemsRegistry.add("orders_by_size", {
    backend_attribute: "orders_by_size",
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 1.5,
    props: (data) => ({
        title: _t("Shirt orders by size"),
        values: data.orders_by_size,
    }),
});

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboarditem";
    static components = { PieChart }
    static props = {
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        }
    }
}
