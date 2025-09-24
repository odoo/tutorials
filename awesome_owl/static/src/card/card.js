import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        content: { optional: true },
        slots: Object,
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen ^= 1;
    }
}
