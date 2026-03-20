import { useState, Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: {type: String},
        slots: Object,
    };

    setup() {
        this.state = useState({ isVisible: true });
    }

    toggleContent() {
        this.state.isVisible = !this.state.isVisible;
    }
}
