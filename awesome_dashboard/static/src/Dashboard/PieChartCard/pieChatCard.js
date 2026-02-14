import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/pieChart";


export class PieChartCard extends Component {
    static components = { PieChart };
    static template = "awesome_dashboard.PieChartCard";
}
