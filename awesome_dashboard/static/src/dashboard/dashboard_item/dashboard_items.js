import { _t } from "@web/core/l10n/translation";
import { NumberCard } from "./cards/number_card";
import { PieChartCard } from "./cards/pie_chart_card";
import { registry } from "@web/core/registry";

const dashboardItems = [
    {
        id: "average_quantity",
        description: _t("Average amount of t-shirt"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            number: data.average_quantity
        }),
    },
    {
        id: "average_time",
        description: _t("Average time for an order to go complete"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            number: data.average_time
        }),
    },
    {
        id: "nb_new_orders",
        description: _t("Number of new orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            number: data.nb_new_orders
        }),
    },
    {
        id: "nb_cancelled_orders",
        description: _t("Number of cancelled orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            number: data.nb_cancelled_orders
        }),
    },
    {
        id: "total_amount",
        description: _t("Total amount of new orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            number: data.total_amount
        }),
    },
    {
        id: "orders_by_size",
        description: _t("Shirt orders by size"),
        Component: PieChartCard,
        props: (data) => ({
            label: _t("Shirt orders by size"),
            data: data.orders_by_size
        }),
    },
]

dashboardItems.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item)
})