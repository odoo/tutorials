/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    // Define the expected props for this component
    static props = {
        // onChange is an optional prop (usually a callback function passed from parent)
        onChange: { type: Function, optional: true },
    };

    // Called when the component is initialized
    setup() {
        // Define the reactive state for this component — holds current count value
        this.state = useState({ count: 0 });
    }

    // This method is triggered when the user clicks the increment button
    increment() {
        // Increase the local count state by 1
        this.state.count++;

        // If the parent provided an `onChange` callback, call it
        // This allows the child to inform the parent that a change occurred
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
