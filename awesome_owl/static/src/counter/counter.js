import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
    static template = xml`
        <div>
            <p>Counter: <t t-esc="state.value"/></p>
            <button class="btn btn-primary" t-on-click="increment">Increment</button>
        </div>
    `;

    static props = {
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        this.props.onChange?.();
    }
}
