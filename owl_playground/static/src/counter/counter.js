/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "owl_playground.Counter";
  setup() {
    this.state = useState({ value: 1 });
  }
  increment() {
    this.state.value++;
  }
}
