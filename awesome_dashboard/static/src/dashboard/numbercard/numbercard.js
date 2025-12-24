import { Component } from "@odoo/owl";
export class Numbercard extends Component {
  static template = "awesome_dashboard.Numbercard";
  static props = {
    title: { type: String },
    value: { type: [String,Number] },
  };
}
