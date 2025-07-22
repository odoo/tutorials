import { PieChart } from "@awesome_dashboard/dashboard/components/piechart/piechart";
import { Component } from "@odoo/owl";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = ["title", "data"];
}
