import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.Counter";

  setup() {
    // extra : tried passing props value from parent without validation
    // Component 'Counter' does not have a static props description
    this.state = useState({ value: this.props.value ? this.props.value : 0 });
  }

  increment() {
    this.state.value++;
  }
}
