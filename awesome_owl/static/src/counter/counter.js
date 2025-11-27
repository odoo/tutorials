import { Component, useState } from "@odoo/owl";


export class Counter extends Component {
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ counter: 1 });
    }

    incrementCounter() {
        this.state.counter++;
        this.props.callback();
    }

    static props = { callback: Function };

}
