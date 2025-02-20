import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props ={ incrementsum:{type:Function} }

    setup() {
        this.state = useState({ value: 0 });
    }
    increment() {
        this.state.value++;
        this.props.incrementsum();
    }
}
