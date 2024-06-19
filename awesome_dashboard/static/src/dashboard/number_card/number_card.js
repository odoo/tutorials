/** @odoo-module **/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
  static props = {
    header: String,
    value: Number,
  };
  static template = "awesome_dashboard.number_card";
}
