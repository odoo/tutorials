/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    state = useState({ count: 1 });

    increment() {
        this.state.count++;
    }
}