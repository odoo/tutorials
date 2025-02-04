import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static props = ['onChange?'];
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        // this.props.onChange();
    }
}