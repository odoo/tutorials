import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange(1);
        }
    }

    decrement() {
        if (this.state.value > 0){
        this.state.value--;
        if (this.props.onChange) {
            this.props.onChange(-1);
        }
        }
    }
}
