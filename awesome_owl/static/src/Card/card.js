import { useState, Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String },
        slots : { type: Object, optional: true },
    };

    setup() {
        this.state = useState({ isOpened: true });
    }

    toggleCard() {
        this.state.isOpened = !this.state.isOpened;
    }
}
