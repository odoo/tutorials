/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: { optional: true },
        index: { type: Number, optional: false },
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange(this.props.index, this.state.value);
        }
    }
}
