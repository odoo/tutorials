/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    
    static template = "my_module.Counter";

    static props = {
        onchange: {type: Function, optional: true}
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if (this.props.onchange != null)
            this.props.onchange(this.state.value);
    }
}