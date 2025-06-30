/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";

export class AwesomeDashboardItem extends Component {
  static template = "awesome_dashboard.AwesomeDashboardItem";
  static components = { Layout };
  static props = {
    slots: {
      type: Object,
      shape: {
        default: Object,
      },
    },
    size: {
      type: Number,
      default: 1,
      optional: true,
    },
  };

  setup() {}
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboardItem", AwesomeDashboardItem);
