import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.counter";

  static props = {
    onChange:Function
  }

  setup() {
    this.count = useState({ value: 0 });
  }
  increment() {
    this.count.value++;
  }
}
