import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        onChange: { type: Function, optional: true },
        onChanges: { type: Function, optional: true }
    };

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
        if (this.props.onChange)
            this.props.onChange();
    }

    decrement() {
        this.state.value--;
        if (this.props.onChanges)
            this.props.onChanges();
    }
}
