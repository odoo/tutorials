/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "owl_playground.counter";

    setup() {
        this.state = useState({ value: 22 });
    }

    increment() {
        this.state.value++;
    }

}
