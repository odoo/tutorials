import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {type: String},
        slots: {
            type: Object,
            shape: {
                default: true
            }
        }
    };

    setup() {
        this.isOpen = useState({ toggleOpen: true });
    }

    toggleCard() {
        this.isOpen.toggleOpen = !this.isOpen.toggleOpen;
    }
}
