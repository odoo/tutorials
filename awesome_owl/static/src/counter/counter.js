import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    static props = {
        onChange: { type: Function, optional: true },
        max: { type: Number, optional: true },
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        if (this.props.max !== undefined && this.state.value >= this.props.max) {
            return;
        }
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }

    decrement() {
        if (this.state.value > 0) {
            this.state.value--;
            if (this.props.onChange) {
                this.props.onChange(this.state.value);
            }
        }
    }

    reset() {
        this.state.value = 0;
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }
}
