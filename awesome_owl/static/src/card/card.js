/** @odoo-module **/

import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";

    setup() {
        this.state = useState({ open: true });
    }

    static props = {
        title: String,
        slots: {
            default: Component
        }
    };

    toggleCard() {
        this.state.open = !this.state.open;
        console.log("Clicked!!")
    }
}
