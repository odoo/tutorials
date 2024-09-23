/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter.counter";
    static props = {
        onChange: {
            type: Function,
            optional: true,
        },
    }

    setup() {
        this.counter = useState({ value: 0 });
    };

    updateValue(newValue) {
        let oldValue = this.counter.value;
        this.counter.value = newValue;
        if (this.props.onChange) {
            this.props.onChange(this, oldValue);
        }
    }

    increment() {
        this.updateValue(this.counter.value + 1);
    }
    decrement() {
        this.updateValue(this.counter.value - 1);
    }
}