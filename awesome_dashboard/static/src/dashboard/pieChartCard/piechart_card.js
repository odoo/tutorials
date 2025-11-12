import { Component } from "@odoo/owl";
import { PieChart } from "./pieChart/piechart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.piechartcard";
    static components = {PieChart};
    static props = {
        title: { type: String },
        value: { type: Number },
    };
}
