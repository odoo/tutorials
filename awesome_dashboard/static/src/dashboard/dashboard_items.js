
import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card";

const dashboardRegistry = registry.category("awesome_dashboard");
console.log(dashboardRegistry);


dashboardRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total Orders",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Total Orders",
        value: data.total_amount,
    }),
});

dashboardRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average Quantity",
    Component: NumberCard,
    size: 1,
    props: (data) => ({
        title: "Average Quantity",
        value: data.average_quantity,
    }),
});

dashboardRegistry.add("sales_by_size", {
    id: "sales_by_size",
    description: "Sales by T-shirt Size",
    Component: PieChartCard,
    size: 3,
    props: (data) => ({
        title: "Sales by T-shirt Size",
        labels: data.qty_by_size.labels,
        values: data.qty_by_size.values,
    }),
});
