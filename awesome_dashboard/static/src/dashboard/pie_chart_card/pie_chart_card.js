import { Component, useProps, types as t } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };

    props = useProps({
        title: t.string(),
        values: t.object(),
    })
}