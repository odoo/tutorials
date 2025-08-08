import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        onChange: { type: Function, optional: true }
    };
    setup() {
        this.state = useState({ finalValue: 0 });
    }
    increment() {
        this.state.finalValue++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}