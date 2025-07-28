/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {type: String},
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    };

    setup() {
        this.state = useState({ open: true });
    }

    toggleState() {
        this.state.open = !this.state.open;
    }
}
