import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    setup() {
        this.state = useState({ value: 1 });
    }
    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }

    static props = ["onChange?"]
    static template = "awesome_owl.counter";
}
