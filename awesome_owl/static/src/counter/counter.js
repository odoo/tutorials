import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        callback: Function
    }

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        this.props.callback(this.state.value);
    }


}