import {Component, useState} from "@odoo/owl";

export class Counter extends Component {
    static template = "counter.Counter";

    setup() {
        this.state = useState({value: 0})
    }

    increment() {
        this.state.value++;
    }

    decrement() {
        this.state.value--;
    }
}