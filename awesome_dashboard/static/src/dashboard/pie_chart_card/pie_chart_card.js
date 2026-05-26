import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.piechartcard";
    static components = { PieChart };
    static props = {
        title: { type: String },
        chart_data: { type: Object },
        clickPie: { type: Function, optional: true },
    };
}
