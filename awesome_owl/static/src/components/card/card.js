import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static template = "awsome_owl123.Card";
    static props = {
        title: { type: String },
        slots: { type: Object, optional: true },
    };
    setup() {
        this.state = useState({ open: true });
    }
    toggle() {
        this.state.open = !this.state.open;
    }
}
