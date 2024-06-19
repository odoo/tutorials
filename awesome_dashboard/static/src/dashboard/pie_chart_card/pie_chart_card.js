/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
  static props = {
    header: String,
    data: Object,
  };
  static template = "awesome_dashboard.pie_chart_card";
  static components = { PieChart };
}
