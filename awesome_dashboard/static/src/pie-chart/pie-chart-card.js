import { Component } from "@odoo/owl";
import { PieChart } from "./pie-chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.pie-chart-card";
    static props = {
        title: String,
        value: { type: Object, values: Number },
    };
    static components = { PieChart };
}
