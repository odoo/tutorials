/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
  static template = "awesome_dashboard.dashboard_item";

  static components = {};

  static props = ["size", "title", "value"];

  static defaultProps = {
    size: 1,
  };
}
