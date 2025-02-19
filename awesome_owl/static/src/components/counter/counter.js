import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.counter";

  static props = {
    callbackIncrement: { type: Function },
  };

  setup() {
    this.state = useState({ value: 0 });
  }

  increment() {
    this.state.value += 1;
    this.props.callbackIncrement();
  }
}
