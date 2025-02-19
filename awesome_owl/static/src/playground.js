/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        debugger
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}
