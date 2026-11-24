import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { _t } from "@web/core/l10n/translation";

export class DashboardItem extends Component {

    static template = "awesome_dashboard.Dashboard_item"

    static props = {
        size:{
            type:Number,
            Optional:true
        },
        slots:{
            type:Object,
            shape:{default:true}
        },
    }

    static defaultProps ={
        size:1
    }


}




export const items = [
    {
        id: "nb_new_orders",
        description: _t("Number of new orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("New orders"),
            value: data.nb_new_orders,
            note: _t("this month"),
            color: _t("text-primary"),
        }),
    },
    {
        id: "total_amount",
        description: _t("Total amount of new orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount"),
            value: data.total_amount,
            note: _t("of new orders this month"),
            color: "text-success",
        }),
    },
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt by order this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Avg. t-shirts per order"),
            value: data.average_quantity,
            note: _t("this month"),
            color: "text-info",
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: _t("Number of cancelled orders this month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Cancelled orders"),
            value: data.nb_cancelled_orders,
            note: _t("this month"),
            color: "text-danger",
        }),
    },
    {
        id: "average_time",
        description: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Avg. processing time"),
            value: data.average_time,
            note: _t("from 'new' to 'sent' or 'cancelled'"),
        }),
    },
    {
        id: "orders_by_size",
        description: _t("Orders by t-shirt size"),
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("T-shirts sold by size"),
            data: data.orders_by_size,
        }),
    },
];

const dashboardRegistry = registry.category("awesome_dashboard");
items.forEach((item, index) => {
    dashboardRegistry.add(item.id, item, { sequence: index + 1 });
});
