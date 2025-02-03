import { useState, Component } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState(
            {
                counter: 0
            }
        )
    }
    increment() {
        this.state.counter++;
        this.props.increment();
    }
    decrement() {
        this.state.counter--;
        this.props.decrement();
    }
}