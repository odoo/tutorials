import { Component, useProps, t } from "@odoo/owl";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };

    props = useProps({
        title: t.string(),
        values: t.object(),
    });
}