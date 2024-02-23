/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: { type: Function, optional: true },
    }

    state = useState({ count: 1 });

    increment() {
        this.state.count++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}