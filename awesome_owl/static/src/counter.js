/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Card } from "./card";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static components = { Card }
    static props = {
        onChange: { Function, optional: true },
    }

    setup() {
        this.state = useState({ value: 0 })
    }

    counter_increment() {
        this.state.value++
        if (this.props.onChange) {
            this.props.onChange(this.state.value)
        }
    }

    counter_decrement() {
        return this.state.value <= 0 ? 0 : this.state.value--
    }
}
