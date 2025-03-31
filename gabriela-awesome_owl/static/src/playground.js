/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Playground extends Component {
    static template = "gabriela-awesome_owl.playground";

    setup() {
        this.value = useState({value: 1});
    }

    increment() {
        this.state.value = this.state.value + 1;
    }
    
}
