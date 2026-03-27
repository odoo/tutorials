import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: String,
        value: [Number, String],
    };
}

export class PieChartCard extends Component {
    static components = { PieChart };
    static template = "awesome_dashboard.PieChartCard";
    static props = {
        data: Object,
        title: String,
    };
}