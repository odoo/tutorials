/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static props = { onChange: { type: Function, optional: true } };
    static template = "awesome_owl.counter";

    setup() {
        this.counter = useState({ value: 0 });
    }

    increment() {
        this.counter.value++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
