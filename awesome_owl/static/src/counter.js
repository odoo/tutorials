/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static props = {callback: {type: Function, optional: true}}
    static template = "awesome_owl.counter";

    setup() {
        this.state = useState({ counter: 0 });
    }

    increment() {
        this.state.counter++;
        if (this.props.callBack) {
            this.props.callback("A message to pass ;)")
        }
    }
}
