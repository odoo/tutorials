/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter"; 

    static props = {
        onChange: { type: Function, optional: true }, // Optional onChange callback
    };

    setup() {
        this.state = useState({ count: 1 });
    }

    increment() {
        this.state.count += 1;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
