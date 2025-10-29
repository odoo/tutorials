/** @odoo-module alias=@awesome_owl/counter/Counter default=false**/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        incrementVal: { type: Function, optional: true },
        decrementVal: { type: Function, optional: true },
        showDecr: { type: Boolean, optional: true, default: false }
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value = this.state.value + 1;
        if (this.props.incrementVal) {
            this.props.incrementVal();
        }
    }

    decrement() {
        this.state.value = this.state.value - 1;
        if (this.props.decrementVal) {
            this.props.decrementVal();
        }

    }
}
