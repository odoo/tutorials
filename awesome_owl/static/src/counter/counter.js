import { Component, useState } from "@odoo/owl"

export class Counter extends Component {
    static template = "awesome_owl.counter"
    static props = {
        onIncrease: { type: Function, optional: true } ,
        onDecrease: { type: Function, optional: true } ,
    };

    setup() {
        this.state = useState({ value: 0 })
    }

    increment() {
        this.state.value++;
        if (this.props.onIncrease) {
            this.props.onIncrease(); // Call the passed function
        }
    }

    decrement() {
        this.state.value--;
        if (this.props.onDecrease) {
            this.props.onDecrease(); // Call the passed function
        }
    }
}