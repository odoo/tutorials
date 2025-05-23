/** @odoo-module **/

import { useState, Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}
