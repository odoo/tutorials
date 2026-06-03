import { NumberCard } from "../number/number";
import { PieChartCard } from "../pie_chart/pie_chart_card";
import { _t } from "@web/core/l10n/translation";

import { registry } from "@web/core/registry";

const dashboardRegistry = registry.category("awesome_dashboard");

dashboardRegistry.add(
    "nb_new_orders",
    {
        id: "nb_new_orders",
        description: _t("New Orders This Month"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("New Orders This Month"),
            value: data.nb_new_orders,
        }),
    },
    { sequence: 10 }
);

dashboardRegistry.add(
    "total_amount",
    {
        id: "total_amount",
        description: _t("Total Amount New Orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Total Amount New Orders"),
            value: data.total_amount,
        }),
    },
    { sequence: 20 }
);

dashboardRegistry.add(
    "average_quantity",
    {
        id: "average_quantity",
        description: _t("Avg T-Shirts Per Order"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Avg T-Shirts Per Order"),
            value: data.average_quantity,
        }),
    },
    { sequence: 30 }
);

dashboardRegistry.add(
    "nb_cancelled_orders",
    {
        id: "nb_cancelled_orders",
        description: _t("Cancelled Orders"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Cancelled Orders"),
            value: data.nb_cancelled_orders,
        }),
    },
    { sequence: 40 }
);

dashboardRegistry.add(
    "average_time",
    {
        id: "average_time",
        description: _t("Avg Time New to Sent/Cancelled"),
        Component: NumberCard,
        props: (data) => ({
            title: _t("Avg Time New to Sent/Cancelled"),
            value: data.average_time,
        }),
    },
    { sequence: 50 }
);

dashboardRegistry.add(
    "pie_chart",
    {
        id: "pie_chart",
        description: _t("T-Shirt Sizes"),
        Component: PieChartCard,
        size: 2,
        props: (data) => ({
            title: _t("T-Shirt Sizes"),
            data: data.orders_by_size,
        }),
    },
    { sequence: 60 }
);