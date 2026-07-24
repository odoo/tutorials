import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart };
    static template = "awesome_dashboard.PieChartCard";
    static props = {
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
        title: {type: String},
        values: {type: Object},
        slots: {
            type: Object,
        }
    }
}