import { Component } from "@odoo/owl";
import { PieChart } from "../dashboard_pie_chart/dashboard_pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: String,
        value: Object
    };
}
