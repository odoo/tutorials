import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    // Bonus: prop validation.
    // "slots: true" tells the validator that this component accepts
    // the automatic slots prop Owl injects for slotted children.
    static props = {
        title: String,
        slots: true,
    };

    setup() {
        // State: whether the card content is open (visible) or not.
        // Default is open.
        this.state = useState({
            isOpen: true,
        });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}
