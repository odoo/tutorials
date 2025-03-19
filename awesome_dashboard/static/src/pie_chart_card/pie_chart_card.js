import { PieChart } from "../pie_chart/pie_chart";
import { Component } from "@odoo/owl";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: String,
        value: Object,
    };
}