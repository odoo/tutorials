import { Component } from "@odoo/owl"
import { NumberCard } from "./number_card/number_card"
import { PieChartCard } from "./pie_chart/pie_chart_card"

export const items = [
{
    id: "avg_tshirt",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    props: (data) => ({
        description: "Average amount of t-shirt by order this month",
        data: data.avg_tshirt,
    }),
},
{
    id: "avg_processing_time",
    description: "Average Processing Time",
    size: 2,
    Component: NumberCard,
    props: (data) => ({
        description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        data: data.avg_processing_time,
    }),
},
{
    id: "new_orders",
    description: "New Orders",
    Component: NumberCard,
    props: (data) => ({
        description: "Number of new orders this month",
        data: data.new_orders,
    }),
},
{
    id: "cancelled_orders",
    description: "Cancelled orders",
    Component: NumberCard,
    props: (data) => ({
        description: "Number of cancelled orders this month",
        data: data.cancelled_orders,
    }),
},
{
    id: "shirt_by_size",
    description: "Shirt orders by size",
    size: 3,
    Component: PieChartCard,
    props: (data) => ({
        description: "Shirt orders by size",
        data: data.shirt_by_size,
    }),
},
];