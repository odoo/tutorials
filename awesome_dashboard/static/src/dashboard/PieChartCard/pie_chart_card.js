import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component{
    static template = "awesome_dashboard.piecard_template";
    static components = { PieChart }
    static props = {
        title : {type: String},
        value : {type: Object}
    };
}
