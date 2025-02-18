import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.counter";

  static props = { label: String };

  setup() {
    this.state = useState({ value: 0 });
  }
  increment() {
    this.state.value++;
  }
}
