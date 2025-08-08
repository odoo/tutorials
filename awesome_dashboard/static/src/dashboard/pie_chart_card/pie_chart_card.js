import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_owl.pie_chart_card";
    static props = {
        title: String,
        values: Object,
    };
    static components = { PieChart };
}
