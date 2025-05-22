/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "@awesome_dashboard/dashboard/charts/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: { type: String, optional: true },
        chart: { type: Object, optional: true, shape: { ...PieChart.props } },
    };
}
