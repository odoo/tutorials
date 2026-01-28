import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {default: Object}
        }
    }

    setup() {
        this.state = useState({ open: true });
    }

    toggleOpen() {
        this.state.open = !this.state.open;
    }
}
