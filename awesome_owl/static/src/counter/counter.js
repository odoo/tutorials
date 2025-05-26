/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: { type: Function, optional: true }
    }

    setup() {
        this.state = useState({ value: 1 });
        
        onMounted(() => {
            if (this.props.onChange != null) {
                this.props.onChange();
            }
        })
    }

    increment() {
        this.state.value += 1;
        if (this.props.onChange != null) {
            this.props.onChange();
        }
    }
}
