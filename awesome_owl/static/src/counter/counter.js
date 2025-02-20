import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChangeIncrease: { type: Function, optional: true },  
        onChangeDecrease: { type: Function, optional: true },  
    }

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        if (this.props.onChangeIncrease) {
            this.props.onChangeIncrease();
        }
    }

    decrement() {
        this.state.value--;

        if (this.props.onChangeDecrease) {
            this.props.onChangeDecrease();
        }
    }
}
    