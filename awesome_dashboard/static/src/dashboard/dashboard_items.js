/** @odoo-module **/

import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./piechart_card/piechart_card";
import { registry } from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        size: 1.3,
        props: (data) => ({
            title: "Avg. T-shirts per Order",
            value: data.average_quantity,
        }),
    },
    {
        id: "sales_distribution",
        description: "Sales distribution",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: "Sales Distribution",
            chartId: "sales-pie-chart",
            data: {
                labels: ["Shirts", "Pants", "Shoes"],
                datasets: [
                    {
                        data: [
                            data.shirts || 0,
                            data.pants || 0, 
                            data.shoes || 0 
                        ],
                    },
                ],
            },
        }),
    },
    {
        id: "Total_orders",
        description: "Orders distribution",
        Component: PieChartCard,
        size: 1,
        props: (data) => ({
            title: "Total Orders",
            chartId: "orders-pie-chart",
            data: {
                labels: ["shirts", "tops", "kurtis"],
                dataset: [
                    {
                        data: [data.shirts, data.tops, data.kurtis],
                        // backgroundColor: ["#d63384", "#20c997", "#6f42c1"]
                    },
                ],

            },
        }),
    }
];
items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
