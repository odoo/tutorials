/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static props = {
        onChange: { type: Function },
        decrement: { type: Function }
    };

    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        this.props.onChange();
    }

    decrement() {
        this.state.value--;
        this.props.decrement();
    }
}
