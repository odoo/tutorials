import {registry} from "@web/core/registry";
import {NumberCard} from "@awesome_dashboard/dashboard/number_card/number_card";
import {PieChartCard} from "@awesome_dashboard/dashboard/pie_chart_card/pie_chart_card";
import {_t} from "@web/core/l10n/translation";

registry.category("awesome_dashboard").add("number_new_orders", {
    id: "number_new_orders",
    description: _t("New orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("New orders this month"),
        value: data.nb_new_orders,
    }),
});

registry.category("awesome_dashboard").add("number_cancelled_orders", {
    id: "number_cancelled_orders",
    description: _t("Cancelled orders this month"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Cancelled orders this month"),
        value: data.nb_cancelled_orders,
    }),
});

registry.category("awesome_dashboard").add("number_total_amount", {
    id: "number_total_amount",
    description: _t("Total amount of orders"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Total amount of new orders this month"),
        value: data.total_amount,
    }),
});

registry.category("awesome_dashboard").add("average_quantity", {
    id: "average_quantity",
    description: _t("Average quantity per order"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average quantity of t-shirts by order"),
        value: data.average_quantity,
    }),
});

registry.category("awesome_dashboard").add("average_time", {
    id: "average_time",
    description: _t("Average time to process"),
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled' (in hours)"),
        value: data.average_time,
    }),
});

registry.category("awesome_dashboard").add("pie_chart_orders", {
    id: "pie_chart_orders",
    description: _t("Shirt orders by size"),
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        title: _t("Shirt orders by size"),
        values: data.orders_by_size,
    }),
});
