import { Component } from "@odoo/owl";
import { DashboardChart } from "../chart/chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { DashboardChart };
    static props = {
        title: { type: String, required: true },
        values: { type: Object, required: true },
        // label: { type: String, optional: true, default: "Dataset" },
    };
}
