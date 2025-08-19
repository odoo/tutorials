/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        onChange: { type: Function }
    };

    setup() {
        this.state = useState({ value: 1 });
    }
    
    increment() {
        this.state.value++;
        if (this.props.onChange)
            this.props.onChange();
    }
}