import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.counter";

  static props = {
    callbackIncrement: { type: Function, optional: true },
  };

  setup() {
    this.state = useState({ value: 0 });
  }

  increment() {
    this.state.value += 1;
    if (this.props.callbackIncrement) {
      this.props.callbackIncrement();
    }
  }
}
