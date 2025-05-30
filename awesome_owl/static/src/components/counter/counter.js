// static/src/components/counter.js
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
static template = "component_counter";
static props = {
  title: String,
  onChange: { type: Function, optional: true },
};

  setup() {
    this.state = useState({ value: 1 });
  }

  increment() {
    this.state.value++;
    if (this.props.onChange) {
      this.props.onChange(this.state.value);
    }
  }

  decrement() {
    this.state.value--;
    if (this.props.onChange) {
      this.props.onChange(this.state.value);
    }
  }
}
