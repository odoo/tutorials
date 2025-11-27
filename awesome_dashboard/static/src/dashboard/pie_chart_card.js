import { Component } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: {
            type: String,
        },
        items: {
            type: Object,
            optional: true,
            default: { m: 0, s: 0, xl: 0 },
        },
    };
}
