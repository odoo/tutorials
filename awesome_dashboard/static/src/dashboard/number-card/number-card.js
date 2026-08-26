import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard-item/dashboard-item";

export class NumberCard extends Component {
  static template = "awesome_dashboard.number_card";
  static props = ['title', 'value'];
  static components = { DashboardItem };
}
