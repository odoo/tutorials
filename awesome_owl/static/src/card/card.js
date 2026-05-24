import { Component, useState } from '@odoo/owl';


export class Card extends Component {
    static template = "card";

    static props = {
        title: { type: String },
        slots: {
            type: Object,
            shape: {
                default: true
            },
            optional: true
        }
    }

    setup() {
        this.state = useState({ isOpen: false })
    }

    cardOpen() {
        this.state.isOpen = !this.state.isOpen;
    }
}
