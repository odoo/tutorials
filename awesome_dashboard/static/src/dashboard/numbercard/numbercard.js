import { Component } from "@odoo/owl";
export class Numbercard extends Component {
  static template = "awesome_dashboard.Numbercard";
  static props = {
    size: {
      type: Number,
      default: 1,
      optional: true,
    },
    slots: {
      type: Object,
      shape: { default: true },
    },
  };
}
