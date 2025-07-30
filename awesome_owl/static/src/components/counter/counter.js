import { Component, useState } from "@odoo/owl";

export class Counter extends Component {

    static template = "awesome_owl.Counter";
    static components = {}
    static props = {
        onChange: {
            type: Function,
            optional: true
        }
    }

    setup() {
        super.setup();
        this.state = useState({ value: 1 })
    }

    increment() {
        this.state.value++;
        this.props.onChange?.(this.state.value);
    }
}
