/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        "title": String, 
        "content": { type: String, optional: true },
        "slots": { type: Object, optional: true },
    };

    setup() {
        this.state = useState({
            isVisible: true  // Stato per controllare la visibilità dello slot
        });
    }

    toggleCard() {
        this.state.isVisible = !this.state.isVisible;
    }
}
