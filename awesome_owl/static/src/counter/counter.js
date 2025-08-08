/** @odoo-module **/

import { useState, Component } from "@odoo/owl"

export class Counter extends Component {
    static props = {
        onChange: {
            type: Function,
            optional: true
        }
    }
    static template = "awesome_owl.counter";

    counterState = useState({ counter: 1 });

    increment() {
        this.counterState.counter++;
        if (this.props.onChange) this.props.onChange()
    }
}
