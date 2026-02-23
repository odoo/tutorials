import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/piechart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: { type: String },
        labels: { type: Array },
        values: { type: Array },
    };
}
