/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true,
            },
        },
    };

    setup() {
        this.isShown = useState({ isShown: true })
    }

    toggle() {
        this.isShown.isShown = !this.isShown.isShown;
    }
}
