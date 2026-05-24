import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/piechart";
export class PieChartCard extends Component {
    static template = "pieChartCard"
    static components = {PieChart}
    static props = {
        title: { type: String },
        value: { type: Object }
    }
}