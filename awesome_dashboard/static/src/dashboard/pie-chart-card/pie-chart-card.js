import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard-item/dashboard-item";
import { PieChart } from "../pie-chart/pie-chart";

export class PieChartCard extends Component {
  static template = "awesome_dashboard.pie_chart_card";
  static props = ['title', 'data'];
  static components = { DashboardItem, PieChart };
}
