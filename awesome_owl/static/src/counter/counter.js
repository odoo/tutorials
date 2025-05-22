/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        title: { type: String, optional: true },
        onIncrement: { type: Function, optional: true },
        slots: { type: Object, optional: true },
    };

    setup() {
        this.state = useState({ count: 0, show: true });
    }

    increment() {
        this.state.count++;
        this.props.onIncrement?.();
    }

    toggleShow() {
        this.state.show = !this.state.show;
    }
}
