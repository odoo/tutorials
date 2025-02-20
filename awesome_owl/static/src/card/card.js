import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card"
    static props = {
        title: { type: String, optional: false},
        slots: { type: Object, optional: true }
    }

    setup() {
        this.contentToggle = useState({ isToggled: true });
    }

    toggleContent() {
        this.contentToggle.isToggled = !this.contentToggle.isToggled;
    }
}
