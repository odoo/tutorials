import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.counter";

  static props = {
    label: {
      type: String,
    },
    onChange: { type: Function, optional: true },
  };

  setup() {
    this.state = useState({ value: 0 });
  }
  increment() {
    this.state.value++;
    if (this.props.onChange) {
      this.props.onChange();
    }
  }
}
