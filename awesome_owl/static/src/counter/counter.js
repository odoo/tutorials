/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter"
    
    static props = { //validation on props
        onChange: {
            type: Function,
            optional: true
        }
    }
    
    setup() { //constuctor
        this.state = useState({ value: 0 });
    }

    increment() {
        this.props.onChange()
        this.state.value++;
    }
}
