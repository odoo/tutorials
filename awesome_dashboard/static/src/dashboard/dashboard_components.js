import { Component } from "@odoo/owl";
import { PieChart } from "./components/pie_chart/pie_chart";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
}

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
}
