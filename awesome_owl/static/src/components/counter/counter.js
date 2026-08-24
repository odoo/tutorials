import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange: {type: Function, optional: true}
    }

    counter = useState({ value: 0 })

    increment() {
        this.counter.value += 1
        this.props.onChange?.()
    }
}
