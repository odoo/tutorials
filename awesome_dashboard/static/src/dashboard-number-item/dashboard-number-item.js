import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard-item/dashboard-item";

export class DashboardNumberItem extends Component {
  static template = "awesome_dashboard.dashboard_number_item";
  static props = ['description', 'number'];
  static components = { DashboardItem };
}
