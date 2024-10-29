import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = 'awesome_owl.card';

    static props = {
        title: { type: String },
        slots: { type: Object, optional: true },
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleIsOpen() {
        this.state.isOpen = !this.state.isOpen;
    }
}
