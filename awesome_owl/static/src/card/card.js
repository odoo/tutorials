/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    static props = {
        title: { type: String, optional: true },
        content: { type: String, optional: true },
        heading: { type: String, optional: true },
        describtion: { type: String, optional: true },
        slots: {type: Object, optional: true, shape: { default: true }},
    };
    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}
