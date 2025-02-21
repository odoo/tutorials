import { Component, useState } from "@odoo/owl";

export class CounterComponent extends Component {
  static props = {
    onChange: { type: Function, optional: true },
  };
  static template = "awesome_owl.counter";
  setup() {
    this.counter = useState({ value: 1 });
  }
  incrementCounter() {
    this.counter.value++;
    if (this.props.onChange) {
      this.props.onChange();
    }
  }
}
