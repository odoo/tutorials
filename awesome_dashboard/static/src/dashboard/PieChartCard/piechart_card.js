import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart }
    static template = "awesome_dashboard.PieChartCard";
    static props = {
        title: String,
        value: Object,
    }
}
