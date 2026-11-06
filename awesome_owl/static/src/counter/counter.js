import {Component, useState} from "@odoo/owl";

export class Counter extends Component {
    static template = "counter.Counter";
    static props = {
        onchange: {
            type: Function,
            optional: true
        }
    };

    setup() {
        this.state = useState({value: 0});
    };

    increment() {
        this.state.value++;
        this.props.onchange?.(true);
    };

    decrement() {
        this.state.value--;
        this.props.onchange?.();
    };
}