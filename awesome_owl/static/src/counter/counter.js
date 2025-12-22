import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter"
    static props = {
        onIncrementCallback: {
            type: Function,
            optional: true
        }
    }

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        if (this.props.onIncrementCallback) {
            this.props.onIncrementCallback()
        }
        this.state.value++;
    }
}
