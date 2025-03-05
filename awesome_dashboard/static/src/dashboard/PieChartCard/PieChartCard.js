import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/PieChart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = {PieChart};

    static props = {
        value: Number,
    };
}
