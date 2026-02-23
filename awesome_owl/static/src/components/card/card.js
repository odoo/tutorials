import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        slots: Object,
    };
    setup() {
        this.state = useState({ isOpen: true });
    }
    toggleOpen() {
        this.state.isOpen = !this.state.isOpen;
    }
}
