import { Component, useState, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    setup() {
        this.footer = markup("<div class='fw-bold text-success'>This is the footer</div>");
        this.state = useState({ isOpen: true });
    }

    static props = {
        title: { type: String },
        slots: { type: Object, optional: true },
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}
