import { Component, useState } from "@odoo/owl"
import { Card } from "../card/card"

export class Counter extends Component {
    static template = "awesome_owl.Counter"
    static components = { Card }
    static props = {
        onChange: { type: Function, optional: true }
    };

    setup() {
        this.state = useState({ 'value': 1 })
    }

    increment() {
        this.state.value++;
        if(this.props.onChange) {
            this.props.onChange();
        }
    }
}
