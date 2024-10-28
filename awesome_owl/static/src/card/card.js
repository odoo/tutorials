/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class Card extends Component {
    static props = {
        toggled: { type: Boolean, optional: true },
        slots: {
            type: Object,
            shape: {
                default: Object,
                name: { type: Object, optional: true },
                action: { type: Object, optional: true },
                counter: { type: Object, optional: true },
            },
        },
    };

    static template = "awesome_owl.card";
    static components = { Counter };

    setup() {
        this.state = useState({ sum: 2, toggled: this.props.toggled ?? false });
    }

    incrementSum() {
        this.state.sum++;
    }

    decrementSum() {
        this.state.sum--;
    }

    toggleContent() {
        this.state.toggled = !this.state.toggled;
    }
}
