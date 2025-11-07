/** @odoo-module */

import { Component } from "@odoo/owl";
import { PieChart } from "./piechart";

// PieChartCard component to display a pie chart with a title
export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };

    // Props expected by the component
    static props = {
        title: {
            type: String, // Title of the chart
        },
        values: {
            type: Object, // Data values for the pie chart
        },
    };
}
