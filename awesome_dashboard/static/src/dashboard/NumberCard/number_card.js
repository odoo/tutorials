/** @odoo-module **/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
  static template = "awesome_dashboard.NumberCard"; // Match template name in XML
  static props = {
    title: { type: String },
    value: { type: Number },
  };
}
