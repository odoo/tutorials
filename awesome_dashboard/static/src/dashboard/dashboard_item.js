/** @odoo-module **/

import { registry } from "@web/core/registry";
import { StandardItem } from "./standard_item/standard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { _t } from "@web/core/l10n/translation";

const dashboardItemRegistry =
    registry.category("awesome_dashboard.items");
    
dashboardItemRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount",
    Component: StandardItem,
    props: (stats) => ({
        title: _t("Total amount of new orders this month"),
        value: stats.data?.total_amount ?? 0,
    }),
});

dashboardItemRegistry.add("new_orders", {
    id: "new_orders",
    description: "New orders",
    Component: StandardItem,
    props: (stats) => ({
        title: _t("Number of new orders this month"),
        value: stats.data?.nb_new_orders ?? 0,
    }),
});

dashboardItemRegistry.add("pie_chart", {
    id: "pie_chart",
    description: "Orders by size",
    Component: PieChart,
    size: 2,
    props: (stats, {openOrdersBySize}) => ({
        title: _t("Shirt orders by size"),
        data: stats.data?.orders_by_size ?? 0,
        onSliceClick: openOrdersBySize,
    }),
});

// Below code is exporting items in a list

// export const items = [
//     {
//         id: "total_amount",
//         description: "Total amount",
//         Component: StandardItem,
//         size: 1,
//         props: (stats) => ({
//             title: "Total amount of new orders this month",
//             value: stats.data?.total_amount,
//         }),
//     },
//     {
//         id: "new_orders",
//         description: "New orders",
//         Component: StandardItem,
//         size: 1,
//         props: (stats) => ({
//             title: "Number of new orders this month",
//             value: stats.data?.nb_new_orders,
//         }),
//     },
//     {
//         id: "pie_chart",
//         description: "Orders by size",
//         Component: PieChart,
//         size: 2,
//         props: (stats) => ({
//             data: stats.data?.orders_by_size,
//         }),
//     },
    
// ];
