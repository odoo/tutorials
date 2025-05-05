import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: { type: String },
        slots: { type: Object, optional: true },
        // content: { type: String }, removed following 13. Generic Card with slots
    };

    setup() {
        this.state = useState({ opened: true });
    }

    toggleOpened() {
        this.state.opened = !this.state.opened;
    }
}
