/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class Card extends Component {
    static props = {
        name: { type: String },
        content: { type: String },
        action: { type: String, optional: true },
    };

    static template = "awesome_owl.card";
    static components = { Counter };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }

    decrementSum() {
        this.state.sum--;
    }
}
