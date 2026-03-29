import {NumberCard} from "../number_card/number_card";
import {PieChartCard} from "../charts/pie_chart_card/pie_chart_card";
import {registry} from "@web/core/registry";
import {_t} from "@web/core/l10n/translation";


registry.category("awesome_dashboard").add("average_quantity", {
    description: _t("Average amount of t-shirt by order this month"),
    Component: NumberCard,
    size: 1.5,
    props: (data) => ({
        title: _t("Average amount of t-shirt by order this month"),
        value: data.average_quantity,
    })
});
registry.category("awesome_dashboard").add("average_time", {
    description: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
    Component: NumberCard,
    size: 2,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: data.average_time,
    })
});
registry.category("awesome_dashboard").add("nb_new_orders", {
    description: _t("Number of new orders this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of new orders this month"),
        value: data.nb_new_orders,
    })
});
registry.category("awesome_dashboard").add("nb_cancelled_orders", {
    description: _t("Number of cancelled orders this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Number of cancelled orders this month"),
        value: data.nb_cancelled_orders,
    })
});
registry.category("awesome_dashboard").add("total_amount", {
    description: _t("Total amount of new orders this month"),
    Component: NumberCard,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount,
    })
});
registry.category("awesome_dashboard").add("orders_by_size", {
    id: "orders_by_size",
    description: _t("Shirt orders by size"),
    Component: PieChartCard,
    props: (data) => ({
        data: data.orders_by_size,
        title: _t("Shirt orders by size"),
    })
});
