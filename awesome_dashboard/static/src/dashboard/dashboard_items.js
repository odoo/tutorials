
import { registry } from "@web/core/registry";
import { PieChart } from "./component/pieChart"; 
import { NumberCard } from "./component/numberCard";
import { _t } from "@web/core/l10n/translation";

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

for (const item of dashboardItems) {
    registry.category("awesome_dashboard.items").add(item.id, item);
}
