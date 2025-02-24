import { Component } from "@odoo/owl";
import { PieChart } from '../pie_chart/piechart';

export class PieChartCard extends Component {

    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: { type: String },
        value: { type: Object },
    };
}
