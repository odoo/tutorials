import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

registry.category("awesome_dashboard").add("numb", {
    Component: NumberCard,
    props: (item) => ({
        title: item.label,
        value: item.value,
    }),
});

registry.category("awesome_dashboard").add("chart", {
    Component: PieChartCard,
    props: (item) => ({
        title: item.label,
        data: item.data,
    }),
});
