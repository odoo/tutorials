import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({
            number: 1,
        })
    }

    increment() {
        this.state.number++;
    }
}
