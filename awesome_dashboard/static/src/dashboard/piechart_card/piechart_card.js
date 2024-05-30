/** @odoo-module */

import {Component} from "@odoo/owl";
import {PieChart} from "../piechart/piechart";
import {DashboardItem} from "../dashboard_item/dashboard_item";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static props = {
        size: Number,
        label: String,
        data: {}
    };

    static components = {DashboardItem, PieChart};
}