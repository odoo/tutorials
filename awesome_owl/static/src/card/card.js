import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: { type: String },
        slots: {
            type: Object,
            shape: { default: true },
        }
    };

    setup() {
        this.state = useState({ toggleCard: true });
    };

    cardtoggle() {
        this.state.toggleCard = !this.state.toggleCard
    };

}
