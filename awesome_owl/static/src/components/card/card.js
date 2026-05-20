import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: Object,
            },
        },
    };

    setup() {
        this.state = useState({ visible: true });
    }

    toggle() {
        this.state.visible = !this.state.visible;
    }
}
