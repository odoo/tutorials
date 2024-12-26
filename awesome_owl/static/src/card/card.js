import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        slots: Object
    }

    setup() {
        this.state = useState({ isOpened: false });
    }

    toggleState() {
        this.state.isOpened = !this.state.isOpened;
    }
}
