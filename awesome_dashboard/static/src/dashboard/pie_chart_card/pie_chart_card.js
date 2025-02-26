// imports
import { Component } from "@odoo/owl";
import { PieChart } from "@awesome_dashboard/dashboard/pie_chart/piechart";

export class PieChartCard extends Component {
    // serves as a wrapper for displaying a PieChart
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: {
            type: String, // Title of the chart
        },
        values: {
            type: Object, // Data values 
        },
    };
}
