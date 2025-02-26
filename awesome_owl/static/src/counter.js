import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        // Initialize a reactive state with a counter starting at 0
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }

    decrement() {
        this.state.count--;
        if (this.props.onChangeM) {
            this.props.onChangeM();
        }
    }

    static props = {
        onChange: {
            type: Function,
            optional: true
        },
        onChangeM: {
            type: Function,
            optional: true
        },
    };
}
