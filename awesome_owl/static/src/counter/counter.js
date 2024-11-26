import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        onIncrement : {type: Function, optional: true}
    }
    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if (this.props.onIncrement) {
            this.props.onIncrement();
        }
    }
  }
