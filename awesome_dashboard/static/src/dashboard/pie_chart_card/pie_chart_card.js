/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { PieChart } from "../../pie_chart/pie_chart";
import { DashboardItem } from "../dashboard_item/dashboard_item";


export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart, DashboardItem }
}
