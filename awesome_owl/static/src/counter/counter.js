/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
    static template = xml`
        <div>
            <p>Counter: <t t-esc="state.value"/></p>
            <button t-on-click="increment">Increment</button>
        </div>
    `;

    static props = {
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }
}
