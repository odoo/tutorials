import { Component, useState } from "@odoo/owl";


export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = {
        onChangeIncrement: { type: Function, optional: true},
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        if (this.props.onChangeIncrement) {
            this.props.onChangeIncrement();
        }
    }

}
