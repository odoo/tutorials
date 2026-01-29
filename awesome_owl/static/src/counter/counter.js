import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        count: { type: Number, optional: true },
        onChange: { type: Function, optional: false },
    };

    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        if (this.props.onChange) {
            this.props.onChange();
        } else {
            this.state.count++;
        }
    }
}
