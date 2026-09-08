import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./piechart_card/piechart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";


const items = [
    {
        id: "average_quantity",
        description: "Average  amount of tshirt",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month "),
            value: data.average_quantity
        })
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
            value: data.average_time
        })
    },
    {
        id: "number_new_orders",
        description: "New Order this month",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of new Order this month"),
            value: data.nb_new_orders
        })
    },
    {
        id: "cancelled_orders",
        description: "Cancelled order this month",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Number of Cancelled order this month"),
            value: data.nb_cancelled_orders
        })
    },
    {
        id: "amount_new_orders",
        description: "Amount orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total amount of new orders this"),
            value: data.total_amount
        })
    },
    {
        id: "pie_chart",
        description: "Shirt orders by size",
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("Shirt orders by size"),
            value: data.orders_by_size,
        })
    }

]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
