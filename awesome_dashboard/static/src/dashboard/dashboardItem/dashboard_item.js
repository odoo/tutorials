/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
  static template = "awesome_dashboard.DashboardItem";
  static props = {
    size: { type: Number, optional: true },
    title: { type: String },
    slots: {
      type: Object,
      optional: true,
      shape: {
        default: true,
      },
    },
  };
  static defaultProps = {
    size: 1,
  };
  setup() {
    super.setup();
  }
}
