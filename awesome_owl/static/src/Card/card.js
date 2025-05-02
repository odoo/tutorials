/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static props = {
        title: String,
        slots: {
            type: Object,
        }
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleIsOpen() {
        this.state.isOpen = !this.state.isOpen;
    }

    static template = "awesome_owl.card";
}
