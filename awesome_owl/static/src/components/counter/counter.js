/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        callback: {
            type: Function,
            optional: true
        }
    }

    setup() {
        this.state = useState({counter: 0});
    }

    increment() {
        this.props.callback();
        this.state.counter++;
    }
}
