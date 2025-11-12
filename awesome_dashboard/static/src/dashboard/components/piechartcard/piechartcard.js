import { Component } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";

export class PieChartCard extends Component{
    static template = "awesome_dashboard.pieChartCard"
    static components = { PieChart }
    static props = {
        desc: String,
        data: Object
    }
}
