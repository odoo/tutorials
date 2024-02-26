/** @odoo-module */

import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
  static template = "awesome_dashboard.PieChartCard";
  static components = { DashboardItem, PieChart };
  static props = {
    title: String,
    data: Object,
  };
}
