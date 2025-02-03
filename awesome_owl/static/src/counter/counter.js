import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        callbackincrement: { type: this.props },
        callbackdecrement: { type: this.props }
    }
    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
        this.props.callbackincrement();
    }

    decrement() {
        this.state.value--;
        this.props.callbackdecrement();

    }
}
