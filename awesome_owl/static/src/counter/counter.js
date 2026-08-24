import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        initialValue: { type: Number, optional: true},
        onChange: { type: Function, optional: true },
        onRegister: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: this.props.initialValue ?? 0});

        if (this.props.onRegister) {
            this.props.onRegister(this)
        }
    }

    increment() {
        this.state.value++;

        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
