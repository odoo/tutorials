import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value = this.state.value + 1;
    }
}
