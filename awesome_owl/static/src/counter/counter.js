/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        title: { type: String, optional: true },
        extraContent: { type: String, optional: true },
        onIncrement: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
        this.props.onIncrement?.();
    }
}
