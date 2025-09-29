import { Component } from "@odoo/owl";
import { DashboardChart } from "../dashboard_chart";

export class ChartCard extends Component {
    static template = "awesome_dashboard.ChartCard";
    static components = { DashboardChart };
    static props = {
        title: String,
        value: Object,
        type: String,
    }
}
