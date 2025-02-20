import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class Card extends Component {
    static template = "awesome_owl.card";
    static components = { Counter };

    static props = {
        title: { type: String, optional: false },
        slots: { type: Object, optional: true },
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}
