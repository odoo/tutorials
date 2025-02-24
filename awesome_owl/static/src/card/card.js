import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static props = {
        title: { type: String },
        slots: { type: Object }
    }
    static template = "awesome_owl.card"
    setup() {
        this.state = useState({ show: true });
    }
    toggle() {
        this.state.show = !this.state.show;
    }
}
