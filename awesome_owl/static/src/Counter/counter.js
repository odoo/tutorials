import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    static props = {
        callback : { type : Function }
    }

    increment() {
        this.state.value++;
        this.props.callback()
    }
}