import { NumberCard } from "./NumberCard/numberChart";
import { PieChartCard } from "./PieChartCard/pieChatCard"
import { dashboardRegistry } from "./dashboard_registry";
import { _t } from "@web/core/l10n/translation";


dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: _t("Average Amount of T-shirt by order this month"),
    Component: NumberCard,
    size: 1,
    props: (stats) => ({
        title: _t("Average Amount of T-shirt by order this month"),
        value: stats?.average_quantity,
    }),
});

dashboardRegistry.add("average_time", {
    id: "average_time",
    description: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
    Component: NumberCard,
    size: 1,
    props: (stats) => ({
        title: _t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        value: stats?.average_time,
    }),
});

dashboardRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: _t("Number of new orders this month"),
    Component: NumberCard,
    size: 1,
    props: (stats) => ({
        title: _t("Number of new orders this month"),
        value: stats?.nb_new_orders,
    }),
});

dashboardRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: _t("Number of cancelled orders this month"),
    Component: NumberCard,
    size: 1,
    props: (stats) => ({
        title: _t("Number of cancelled orders this month"),
        value: stats?.nb_cancelled_orders,
    }),
});

dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: _t("Total amount of new orders this month"),
    Component: NumberCard,
    size: 1,
    props: (stats) => ({
        title: _t("Total amount of new orders this month"),
        value: stats?.total_amount,
    }),
});

dashboardRegistry.add("pie_chart", {
    id: "pie_chart",
    description: _t("Shirt order by size"),
    Component: PieChartCard,
    size: 2,
    props: (stats) => ({
        title: _t("Shirt order by size"),
        data: stats?.orders_by_size,
    }),
});


// export const items = [
//     {
//         id: "total_amount",
//         description: "Total amount",
//         Component: NumberCard,
//         size: 1,
//         props: (stats) => ({
//             title: "Total amount of new orders this month",
//             value: stats?.total_amount,
//         }),
//     },
//     {
//         id: "Pie_Chart",
//         description: "PieChart",
//         Component: PieChartCard,
//         size: 2,
//         props: (stats) => ({
//             title: "Shirt order by size",
//             data: stats?.orders_by_size,
//         }),
//     },
// ];
