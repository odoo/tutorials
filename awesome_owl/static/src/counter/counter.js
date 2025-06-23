import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        onChange: { type: Function, optional: true }
    };

    setup() {
        this.counter = useState({ count: 1 });
    }

    incrementCounter() {
        this.counter.count += 1;

        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
