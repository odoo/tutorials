/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 0 });
    }


    static props = {
        onChange: { type: Function, optional: true },
    };

    increment() {
        this.state.value += 1;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}