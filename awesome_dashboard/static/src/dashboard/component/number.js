import { Component } from "@odoo/owl";

export class Number extends Component {
  static template = "awesome_dashboard.component.Number"
  static props = {
    title: String,
    value: Number,
  }
}
