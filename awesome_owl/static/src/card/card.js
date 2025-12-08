/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    setup() {
        this.state = useState({
            show: false,
        });
    }

    static props = {
        title: {
            type: String,
            optional: true,
        },
        slots: {
            type: Object,
            shape: {
                default: true
            },
        },
    };

    toggleDisplay() {
        this.state.show = !this.state.show;
    }
}
