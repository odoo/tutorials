import { NumberCard } from "./numbercard/numbercard";
import { PieChartCard } from "./piechartcard/piechartcard";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

const items = [
    {
        id: "nb_new_orders",
        description: _t("The number of new orders, this month"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: _t("New Orders This Month:"),
            value: data.data.nb_new_orders
        }),
    },
    {
        id: "total_amount",
        description: _t("The total amount of orders, this month"),
        Component: NumberCard,
        size: 2,
        props: (data) => ({
            title: "Total Amount This Month:",
            value: data.data.total_amount
        }),
    },
    {
        id: "average_quantity",
        description: _t("The average number of t-shirts by order"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: _t("Avg. T-Shirts per Order:"),
            value: data.data.average_quantity
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: _t("The number of cancelled orders, this month"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: _t("Cancelled Orders:"),
            value: data.data.nb_cancelled_orders
        }),
    },
    {
        id: "average_time",
        description: _t("The average time (in hours) elapsed between the moment an order is created, and the moment is it sent"),
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: _t("Avg. Time New → Sent/Cancelled:"),
            value: data.data.average_time
        }),
    },
    {
        id: "orders_by_size",
        description: _t("Number of shirts ordered based on size"),
        Component: PieChartCard,
        size: 3,
        props: (data) => ({
            title: _t("Shirt orders by size:"),
            value: data.data.orders_by_size
        }),
    }
]
items.forEach((item) => {
    registry.category("awesome_dashboard").add(item.id, item)
});
