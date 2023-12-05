/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Playground extends Component {
  static template = "owl_playground.counter";

  setup() {
    this.state = useState({ value: 0 });
  }

  increment() {
    this.state.value++;
  }
}
