import { Component, useState } from "@odoo/owl"

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    setup() {
        this.state = useState({ value: 1 })
    }

    handleIncrement() {
        this.state.value += 1;
        this.props.onCounterIncrement();
    };
}
