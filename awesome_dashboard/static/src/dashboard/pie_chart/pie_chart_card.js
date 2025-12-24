import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_tem";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.pie_chart_card"
    static components = { DashboardItem, PieChart }
    static props = {
        description: String,
        data: Object,
        size: {
            type: Number,
            optional: true
        },
    }
}