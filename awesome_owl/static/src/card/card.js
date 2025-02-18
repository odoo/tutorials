/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card"; // Reference to the template
    setup() {
        this.state = useState({
          isOpen: true,  // Initially, the card content is visible
        });
    }
    static props = {
        title: String,
        slots: {
            type: Object,
            shape : {
                default: true
            },
        }
    };
    toggleCard() {
        // Flip the state to open or close the card
        this.state.isOpen = !this.state.isOpen;
    }
}
