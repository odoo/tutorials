import { _t } from "@web/core/l10n/translation";
import { ChartCard } from "./ChartCard/ChartCard";
import { NumberCard } from "./NumberCard/NumberCard";
import { registry } from "@web/core/registry";

const items = [
    {
        id:"avg_amount",
        description: _t("Average amount of t-shirt by order this month"),
        Component : NumberCard,
        size: 35,
        props: (data) => ({
            title: _t("Average amount of t-shirt by order this month"),
            value: data.average_quantity,
        })
    },
    {
        id:"avg_time",
        description: _t("Average time for an order"),
        Component : NumberCard,
        size: 35,
        props: (data) => ({
            title: _t("Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’"),
            value: data.average_time
        })
    },
    {
        id:"nb_cancelled_orders",
        description: _t("Number of cancelled orders this month"),
        Component : NumberCard,
        size: 25,
        props: (data) => ({
            title: _t("Number of cancelled orders this month"),
            value: data.nb_cancelled_orders
        })
    },
    {
        id:"nb_new_orders",
        description: _t("Number of new orders this month"),
        Component : NumberCard,
        props: (data) => ({
            title: _t("Number of new orders this month"),
            value: data.nb_new_orders
        })
    },
    {
        id:"total_amount",
        description: _t("Total amount of new orders this month"),
        Component : NumberCard,
        size: 45,
        props: (data) => ({
            title: _t("Total amount of new orders this month"),
            value: data.total_amount
        })
    },
    {
        id:"orders_by_size",
        description: _t("Shirt by size"),
        Component : ChartCard,
        size: 25,
        props: (data) => ({
            title: _t("Shirt by size"),
            label : _t("Shirt by size"),
            data : data.orders_by_size,
        })
    },  
]
items.forEach(item => {
        registry.category("awesome_dashboard").add(item.id, item);   
});
    



