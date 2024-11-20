/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static props = {
        increment: { type: Function },
        decrement: { type: Function }
    };

    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        this.props.increment();
    }

    decrement() {
        this.state.value--;
        this.props.decrement();
    }
}
