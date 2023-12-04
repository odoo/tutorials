/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "owl_playground.Counter";

    state = useState({ value: 0 });

    increment() {
        this.state.value++;
    }
}
