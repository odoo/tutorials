/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    debugger;
    increment() {
        this.state.value++;
    }
}   