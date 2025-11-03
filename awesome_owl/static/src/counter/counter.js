import { Component, useState } from "@odoo/owl";


export class Counter extends Component {
    static template = "awesome_owl.counter";
    static defaultProps = {
        buttonText: "Increment",
    }
    static props = {
        buttonText: { type: String, optional: true, },
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
        this.props.onChange?.();
    }
}
