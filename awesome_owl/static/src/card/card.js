/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String, optional: true, default: "Card Title" },
        slots: {type: Object, optional: true},
    };

    setup() {
        // Add state to track if card is open (default: true)
        this.state = useState({ isOpen: true });
    }

    toggleOpen() {
        // Toggle the open/closed state
        this.state.isOpen = !this.state.isOpen;
    }
}