/** @odoo-module **/

import { useState, Component } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    state = useState({count : 0});

    increment() {
        this.state.count++;
    }
}
