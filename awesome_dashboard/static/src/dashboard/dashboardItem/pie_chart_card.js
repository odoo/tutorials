/** @odoo-module **/
import { Component } from "@odoo/owl";
import { PieChart } from "../PieChart/pie_chart";  // Assuming PieChart component is already implemented

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";

    static props = {
        label: String,
        data: Object,  // Data should be an object with t-shirt sizes and their counts
    };

    static components = {
        PieChart,
    };
}
