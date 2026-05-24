// import { Component } from "react";
import { NumberCard } from "./NumberCard/number_card";
import { PieChartCard } from "./PieChartCard/pie_chart_card";
import { registry } from "@web/core/registry"

const items = [
    {
        id: "average_quantity",
        description: "the average number of t-shirts by order",
        component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        })
    },
    {
        id: "average_time",
        description: "the average time (in hours) elapsed between the moment an order is created, and the moment is it sent",
        component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’",
            value: data.average_time
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "the number of cancelled orders, this month",
        component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders
        })
    },
    {
        id: "nb_new_orders",
        description: "the number of new orders, this month",
        component: NumberCard,
        props: (data) => ({
            title: "Number of new orders this month",
            value: data.nb_new_orders
        })
    },
    {
        id: "total_amount",
        description: "the total amount of orders, this month",
        component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount
        })
    },
    {
        id: "pieChart",
        description: "the number of new orders, this month",
        component: PieChartCard,
        props: (data) => ({
            title: "Order by size",
            value: data.orders_by_size
        })
    }
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
