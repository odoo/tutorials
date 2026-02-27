import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pieChart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";

    static components = { PieChart };

    static props = {
        title: { type: String },
        data: {
            type: Array, element: {
                type: Object, shape: {label: String, value: Number }
            }
        },
    };
}