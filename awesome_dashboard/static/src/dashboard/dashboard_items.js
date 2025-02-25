/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

const dashboardItems = [
    {
        id : "average_quantity",
        description : "Average amount of t-shirt",
        Component : NumberCard ,
        size : 1 ,
        props: (data) => ({
            title : "Avg T-Shirts per Order",
            value : data.average_quantity,
        })
    },

    {
        id: "average_time",
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Avg Processing Time",
            value: data.average_time,
        })
    },

    {
        id: "nb_new_orders",
        description: "Number of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "New Orders",
            value: data.nb_new_orders,
        })
    },

    {
        id: "total_amount",
        description: "Total amount--> of new orders this month",
        Component: NumberCard,
        size: 1.3,
        props: (data) => ({
            title: "Total Revenue",
            value: data.total_amount,
        })
    },

    {
        id: "orders_by_size",
        description : "Shirt Orders by Size",
        Component: PieChartCard,
        size : 2,
        props: (data) => ({
            title: "Shirt Orders by Size",
            data : data.orders_by_size
        })
    }
];

dashboardItems.forEach(item => {
    registry.category("awesome_dashboard.items").add(item.id, item);
});
