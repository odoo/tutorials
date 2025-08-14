/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "gabriela-awesome_owl.counter";
    static props = {
        onChange: { type: Function, optional: true}
    };
    
    setup() {
        this.state = useState({ count: 0 });
    }
    
    increment() {
        this.state.count++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}