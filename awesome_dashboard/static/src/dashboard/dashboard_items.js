/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./components/number_card/number_card";
import { PieChart } from "./components/pie_chart/pie_chart";
import { _t } from "@web/core/l10n/translation";
// List of items to register
const dashboardItems = [
    {
        id: "nb_new_orders",
        description: _t("Number of new orders"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: _t("New Orders This Month"),
            value: data.nb_new_orders,
        }),
    },
    {
        id: "total_amount",
        description: _t("Total order amount"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total Order Amount",
            value: data.total_amount,
        }),
    },
    {
        id: "average_quantity",
        description: _t("Average t-shirt quantity"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: _t("Avg T-shirts per Order"),
            value: data.average_quantity,
        }),
    },
    {
        id: "nb_cancelled_orders",
        description:_t("Cancelled Orders"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Cancelled Orders",
            value: data.nb_cancelled_orders,
        }),
    },
    {
        id: "average_time",
        description: _t("Avg processing time"),
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Avg Time to Ship/Cancel",
            value: data.average_time + " min",
        }),
    },
    {
        id: "pie_chart",
        description:_t("Orders by size"),
        Component: PieChart,
        size: 2,
        props: (data) => ({ data: data.orders_by_size }),
    },
];

// Register each item
for (const item of dashboardItems) {
    registry.category("awesome_dashboard.items").add(item.id, item);
}
