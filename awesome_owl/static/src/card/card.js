import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static props = ["title", "slots"];
    static template = "awesome_owl.card";

    setup() {
        this.state = useState({
            isOpen: false,
        });
    }

    toggle() {
        this.state.isOpen = !this.state.isOpen;
    }
}