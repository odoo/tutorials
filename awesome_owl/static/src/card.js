import { Component, markup, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card_template";
    static props = {
        title: { type: String },
        content: { type: String },
        slots: { type: Object, optional: true }
    };

    setup() {
        this.isOpen = useState({ value: true });
    }

    get safeContent() {
        return markup(this.props.content);
    }

    toggleContent() {
        this.isOpen.value = !this.isOpen.value;
    }
}
