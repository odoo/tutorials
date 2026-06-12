import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        slots: {
            type: Object,
            shape: {
                default: true,              // default slot required
                title: { optional: true },  // title slot optional

            }
        }

    };

    setup() {
        this.state = useState({ isOpen: false })
    }

    toggleState() {
        this.state.isOpen = !this.state.isOpen

    }
}
